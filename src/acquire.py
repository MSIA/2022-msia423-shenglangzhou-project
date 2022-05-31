"""
This module contains multiple functions that offers
importing and cleaning functionality
"""
import logging

import pandas as pd

logger = logging.getLogger(__name__)

pd.options.mode.chained_assignment = None


def import_application_data(path):
    """Read data from "path" into a DataFrame and change column names to lower case

    Args:
        path (str): file name path; default value is 'data/sample/application_data.csv'
            (specified in config.yaml)


    Returns:
        data (:obj:`DataFrame <pandas.DataFrame>`): a DataFrame of loan records

    """
    data = pd.read_csv(path)
    logger.info('Data loaded from path: %s', path)
    logger.info("The shape of the DataFrame loaded is: %s", data.shape)

    
    return data

def import_credit_data(path):
    """Read data from "path" into a DataFrame and change column names to lower case

    Args:
        path (str): file name path; default value is 'data/sample/application_data.csv'
            (specified in config.yaml)


    Returns:
        data (:obj:`DataFrame <pandas.DataFrame>`): a DataFrame of loan records

    """
    data = pd.read_csv(path)
    logger.info('Data loaded from path: %s', path)
    logger.info("The shape of the DataFrame loaded is: %s", data.shape)

    
    return data


def filna(df, col, val):
    """Fill the specified column's missing values with specified value

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): a DataFrame of loan records
        col (str): a column in the DataFrame that needs to fill its missing values with 0

    Returns:
        df (:obj:`DataFrame <pandas.DataFrame>`): a resulting DataFrame where the specified
            column has missing values filled with 0

    """
    logger.debug("The column that fills missing values is %s", col)

    df.loc[:, col] = df[col].fillna(val)

  

    return df


def clean_column(df, col, replace_dict):
    """Clean the specified column in the DataFrame with less categories

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): DataFrame with the specified column uncleaned
        col (str): the column which contains categories that needs to be cleaned
        replace_dict (dict of {str : str}): a dictionary that stores the information
            about what to change certain categories into; keys are old categories
            whereas values are new categories

    Returns:
        df (:obj:`DataFrame <pandas.DataFrame>`): a resulting DataFrame with the
            categorical column cleaned with less categories

    """
    for key, value in replace_dict.items():
        df.loc[:, col] = df[col].apply(lambda x: x.replace(key, value))

    logger.debug("The categorical column cleaned with less categories is %s", col)

    return df


def to_str(df, col):
    """Change values in a certain column to string type

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): input DataFrame with
            the specified column uncleaned
        col (str): the column that needs to turn its values into string

    Returns:
        df (:obj:`DataFrame <pandas.DataFrame>`): a resulting DataFrame with
            the the specified column changed to string type

    """
    df.loc[:, col] = df[col].astype(str)
    logger.info("The values in column %s was changed to string", col)
    return df


def neg_to_pos(df, cols):
    """Change signs of specified columns from negative to positive

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): input DataFrame
            where the specified column has negative values
        cols (:obj:`list`): list of columns that needs to turn
            their values from negative to positive to make more sense

    Returns:
        df (:obj:`DataFrame <pandas.DataFrame>`): a resulting DataFrame
            with the the column values changed to positive

    """
    for col in cols:
        df.loc[:, col] = df[col].apply(lambda x: x*-1)
        logger.info("The values in column %s was changed from "
                    "negative values to positive values", col)
    return df


def replace_cat(df, cat_dict):
    """Replace binary categorical columns by more informative
        binary values to match future user input

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): DataFrame with original binary columns
        cat_dict (dict of dict): dictionary of dictionary where the
            outer key is the column name in the DataFrame,
            inner keys are the original binary categories (e.g. 'Y' & 'N')
            and the inner values are the new binary categories (e.g. 'Yes' & 'No')
            to match future user input

    Returns:
        df (:obj:`DataFrame <pandas.DataFrame>`): a resulting DataFrame
            with the the binary column values changed

    """
    for col, values in cat_dict.items():
        for old, new in values.items():
            df[col] = df[col].apply(lambda x: x.replace(old, new))
        logger.debug("The values in column %s was changed to "
                     "binary categories that match future user input", col)

    return df

def clean_target(df,convert_dict, convert_col,key,val1,val2,val3,new_col):
    df.replace({convert_col: convert_dict}, inplace=True)
    df=df.value_counts(subset=[key, convert_col]).unstack(fill_value=0)
    df.loc[(df[val1] > df[val2]), new_col] = 1
    df.loc[(df[val1] > df[val3]), new_col] = 1
    df.loc[(df[val2] > df[val1]), new_col] = 0
    df.loc[(df[val2] > df[val3]), new_col] = 1
    df.loc[(df[val3] > df[val1]), new_col] = 0
    df.loc[(df[val3] > df[val2]), new_col] = 0
    df[new_col] = df[new_col].astype('int')
    df.drop([val1, val2, val3], axis=1, inplace=True)
    return df



def clean(df, filna_col, clean_col, clean_replace_dict, to_str_list, neg_cols, cat_dict, filna_dict):
    """Clean the input DataFrame to be ready to generate new features from

    Args:
        df (:obj:`DataFrame <pandas.DataFrame>`): a DataFrame of raw loan records
        filna_col (str): a column in the DataFrame that needs to
            fill missing values with 0; default is 'amt_req_credit_bureau_day'
            (specified in config.yaml)
        clean_col (str): the column which contains categories that needs to be cleaned;
            default is 'edu_type' (specified in config.yaml)
        clean_replace_dict (dict of {str : str}): a dictionary that stores
            the information about what to change certain categories into (default in config.yaml)
        to_str_list (str): column that needs to turn its values into string;
            default is 'phone_contactable'(config.yaml)
        neg_cols (:obj: `list`): list of columns that needs to turn their values
            from negative to positive to make more sense;
            default is ['days_birth', 'days_employed', 'days_id_change'] (config.yaml)
        cat_dict (dict of dict): dictionary of dictionary where the outer key
            is the column name in the DataFrame, inner keys are the original
            binary categories (e.g. 'Y' & 'N') and the inner values are
            the new binary categories (e.g. 'Yes' & 'No') to match future user input

    Returns:
        df_out (:obj:`DataFrame <pandas.DataFrame>`): a DataFrame of cleaned loan records

    """
    filna_val = filna_dict[filna_col]
    df_fina = filna(df, filna_col, filna_val)
    df_nona = df_fina.dropna()
    df_clean = clean_column(df_nona, clean_col, clean_replace_dict)
    df_out = neg_to_pos(df_clean, neg_cols)
    for col in to_str_list:
        df_out=to_str(df_out, col)
    df_out = replace_cat(df_out, cat_dict)
    for col in to_str_list:
        df_out=to_str(df_out, col)


    if sum(df_out.isna().sum()) != 0:
        logger.warning('There are still missing values in the cleaned DataFrame')
    else:
        logger.info('There are no missing values after the cleaning steps')

    return df_out

def get_full_df(df1,df2,key):
    df_out = df1.merge(df2, how='inner', on=[key])
    return df_out


