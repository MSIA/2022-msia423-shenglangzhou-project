"""This module contains functions to make prediction on the testset
"""
import logging

import pandas as pd
import sklearn
import sklearn.ensemble
import typing

logger = logging.getLogger(__name__)


def compute_score(
    rf_model, test: pd.DataFrame, target_colname: str, proba_col: str, bin_col: str
) -> None:
    """Score the random forest model and evaluate the model performance

    Args:
        rf_model (:obj:`RandomForestClassifier`): trained random forest model object
        test(:obj:`DataFrame <pandas.DataFrame>`): the test dataframe to generate predictions on
        target_colname(str): the result column that we are classifying (target)

    Returns:
        None

    """
    # predict probability and class for each sample in the test set
    X_test = test.drop([target_colname], axis=1)

    x_names = X_test.columns

    ypred_proba_test = rf_model.predict_proba(X_test[x_names])[:, 1]
    ypred_bin_test = rf_model.predict(X_test[x_names])
    # calculate metrics
    ypred = pd.DataFrame({proba_col: ypred_proba_test, bin_col: ypred_bin_test})

    return ypred
