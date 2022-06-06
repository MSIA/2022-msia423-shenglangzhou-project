import pandas as pd
import numpy as np
import config
import os
import yaml
import argparse
from sklearn.metrics import roc_auc_score, confusion_matrix, accuracy_score, classification_report
import logging
import logging.config
import typing

logger = logging.getLogger('evaluate_performace')

def load_test(test:pd.DataFrame, **kwargs)-> pd.DataFrame:
    '''load test label
    input:
        test (pandas.DataFrame):test data
        y_col:                  name of the y column
    output:
        ytest (pandas.DataFrame):test y
    '''
    try:
        logger.info("Loading test data ...")
        test = pd.read_csv(test)
        ytest = test[kwargs["y_col"]]
        return ytest
    except Exception as ex:
        logger.error(ex)

def load_pred(prediciton:pd.DataFrame, **kwargs) -> typing.Tuple[pd.DataFrame]:
    '''load prediction result
    input:
        prediciton(pandas.DataFrame):   prediction 
    output:
        proba (pandas.DataFrame):       probability prediction
        binary (pandas.DataFrame):      binary prediction
    '''
    try:
        logger.info("Loading prediction ...")
        pred = pd.read_csv(prediciton)
        proba = pred[kwargs["proba_col"]]
        binary = pred[kwargs["bin_col"]]
        return proba, binary
    except Exception as ex:
        logger.error(ex)

def compute_metrics(y_test:pd.DataFrame, ypred_proba_test:pd.DataFrame, ypred_bin_test:pd.DataFrame, **kwargs) -> typing.List[int]:
    '''compute metrics
    input:
        ytest(pandas.DataFrame):   Test Result
        ypred_proba_test(pandas.DataFrame): Probability Result
        ypred_bin_test(pandas.DataFrame):   Binary Result
    output: 
        result([int]):    Result
    '''
    try:
        logger.info("Computing metrics ...")
        metrics = kwargs["metrics"]
        result = {}
        if "auc" in metrics:
            result["auc"] = roc_auc_score(y_test, ypred_proba_test)
        if "confusion" in metrics:
            result["confusion"] = confusion_matrix(y_test, ypred_bin_test)
        if "accuracy" in metrics:
            result["accuracy"] = accuracy_score(y_test, ypred_bin_test)
        if "classification_report" in metrics:
            result["classification_report"] = classification_report(y_test, ypred_bin_test)
        return result
    except ValueError:
        logger.error("Failed to save the evaluation results because "
                     "the DataFrame of evaluation results cannot be appropriately called")


