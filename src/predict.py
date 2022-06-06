"""
This module contains multiple functions that offers
user input transformation and prediction functionality
"""
import logging

import joblib
import pandas as pd
import numpy as np
import typing

logger = logging.getLogger(__name__)


def transform_input(ui_dict: typing.Dict[str,str], cat_cols:typing.List[str], ohe_cols:typing.List[str])-> pd.DataFrame:
    """Transform the user input from the app to get predictions using the trained model

    Args:
        ui_dict (dict): a dictionary of user input, collected from the app
        cat_cols (:obj: `list`): a list of categorical columns in the initial input
        ohe_cols (:obj: `list`): a list of required columns in the transformed user input DataFrame

    Returns:
        input_new (:obj:`DataFrame <pandas.DataFrame>`): DataFrame that
            stores the transformed user input

    """
    # transform the user input into a pandas DataFrame
    input_df = pd.DataFrame(ui_dict, index=[0])
    logger.debug('Initial Input column names: %s', input_df.columns)

    # change column names to match the one-hot-encoded column names
    for col in cat_cols:
        input_df = input_df.rename(columns={col: col + '_' + str(input_df[col].values[0])})

    # change value to 1 to simulate one-hot encoded result
    for col in input_df.columns:
        if str.isdigit(str(input_df[col].values[0])):
            pass
        else:
            input_df[col] = 1

    # create an empty DataFrame with the required columns in the model
    ohe_empty = pd.DataFrame(columns=ohe_cols)
    input_new = ohe_empty.T.join(input_df.T).fillna(0).T
    logger.debug('Column names after all transformation steps: %s', input_new.columns)
    return input_new


def get_prediction(input_ohe:pd.DataFrame, model_path:str, ohe_cols:typing.List[str]):
    """Get credit card approval prediction for new user input

    Args:
        input_ohe (:obj:`DataFrame <pandas.DataFrame>`): a DataFrame of the transformed user input
        model_path (str): the path to trained model;
            default is 'models/randomforest.joblib' (config.yaml)
        ohe_cols (:obj:`list`): the required columns used in the trained Random Forest Classifier

    Returns:
        [pred_prob, pred_bin] (:obj:`list`): the first object in the list is
            the predicted probability of credit card approval where the second object
            in the list is the predicted class for the applicant

    """
    # load pre-trained model
    try:
        loaded_rf = joblib.load(model_path)
        logger.info('Loaded model from %s', model_path)
    except OSError:
        logger.error('Model is not found from %s', model_path)
    # predict probability of loan_delinquency with the new user input
    pred_prob = np.round(100 * loaded_rf.predict_proba(input_ohe[ohe_cols])[:, 1][0], 2)
    # predict the class with the new user input
    if loaded_rf.predict(input_ohe[ohe_cols]) == 1:
        pred_bin = "Congratulations! the applicant IS LIKELY to be approved for the Credit Card!!!"
    else:
        pred_bin = "Unfortunately, the applicant IS NOT LIKELY to be approved for the Credit Card!!!"
    return [pred_prob, pred_bin]
