"""
This module contains multiple functions that offers
featurizing and one-hot-encoding functionality
"""
import logging

import pandas as pd
import numpy as np
import typing

logger = logging.getLogger(__name__)

pd.options.mode.chained_assignment = None


def day_to_year(df:pd.DataFrame, new_cols_dict:typing.List[str])->pd.DataFrame:
    """Generate features from specified columns where the
        units of calculation was in 'days' to count in 'years'

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): input DataFrame
            with original 'days' columns
        new_cols_dict (dict of {str : str}): a dictionary that
            stores the new and original column names

    Returns:
        df (:obj:`DataFrame <pandas.DataFrame>`): a resulting DataFrame
            with new 'years' columns created

    """
    for key, value in new_cols_dict.items():
        df.loc[:, key] = df[value].apply(lambda x: np.round(x/365))
        logger.info('New column %s created based on original column %s', key, value)
    return df


def create_new_col(df:pd.DataFrame, old_col:str, new_col:str)->pd.DataFrame:
    """Generate a new column based on an original column in the DataFrame

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): input DataFrame of loan applicant records
        old_col (str): the old column to generate new column from
        new_col (str): the new column generated from the 'old_col'

    Returns:
        df (:obj:`DataFrame <pandas.DataFrame>`): a resulting DataFrame with the new column created

    """
    df.loc[:, new_col] = ['Yes' if i >= 0 else 'No' for i in df[old_col]]
    logger.info('New column %s created based on original column %s', new_col, old_col)
    return df


def featurize(df:pd.DataFrame, dty_cols_dict:typing.Dict[str,str], old_col:str, new_col:str)->pd.DataFrame:
    """Generate new features with the given DataFrame

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): input DataFrame
            of cleaned loan applicant records
        dty_cols_dict (dict of {str : str}): a dictionary that stores
            the new and original column names for changing units of calculation
            from 'days' to 'years' (default in config.yaml)
        old_col (str): the old column to generate 'new_col' from;
            default is 'days_employed' (config.yaml)
        new_col (str): the new column generated from the 'old_col';
            default is 'Employed' (config.yaml)

    Returns:
        df_featurized (:obj:`DataFrame <pandas.DataFrame>`): a resulting DataFrame
            with the new features created

    """
    df_new = day_to_year(df, dty_cols_dict)
    df_featurized = create_new_col(df_new, old_col, new_col)
    logger.info('Feature engineering completed')
    return df_featurized

def get_user_df(df:pd.DataFrame, cat_vars:typing.List[str], num_vars:typing.List[str])->pd.DataFrame:
    '''Get data that could be ingested into RDS
    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): Original DataFrame
        cat_vars (List): List of categorical variables
        num_vars (List): List of Numerical variables
    Returns:
        df_vars (:obj:`DataFrame <pandas.DataFrame>`): Resulting DataFrame
    '''
    df_vars = df[num_vars + cat_vars]
    return df_vars

def get_ohe_data(df:pd.DataFrame, cat_vars:typing.List[str], num_vars:typing.List[str], target_col:str)->pd.DataFrame:
    """One Hot Encode categorical variables in a DataFrame to prepare for modeling

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): input DataFrame of
            featurized loan applicant records
        cat_vars (:obj:`list`): list of categorical columns in the DataFrame
            (default in config.yaml)
        num_vars (:obj:`list`): list of numerical columns in the DataFrame
            (default in config.yaml)
        target_col (str): the target column in the DataFrame; default is 'target'
            (default in config.yaml)

    Returns:
        df_ohe (:obj:`DataFrame <pandas.DataFrame>`): a resulting one-hot-encoded DataFrame

    """
    df_vars = df[num_vars + cat_vars+ [target_col]]
    logger.info('There are %i NUMERICAL variables/features selected', len(num_vars))
    logger.info('There are %i CATEGORICAL variables/features selected', len(cat_vars))


    # create dummies, drop 1 column from each dummy group
    cat_dc = pd.get_dummies(df_vars[cat_vars], drop_first=True)

    # Concatenate encoded columns to numerical columns
    data_ohe = pd.concat([df_vars[num_vars+[target_col]], cat_dc], axis=1)

    return data_ohe
