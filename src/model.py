"""
This module contains multiple functions that offers
model training and model evaluation functionality
"""
import logging

import pandas as pd
import sklearn
import sklearn.ensemble
from imblearn.over_sampling import RandomOverSampler
import typing

logger = logging.getLogger(__name__)



def train_model(data:pd.DataFrame, target_colname:str, sample_strat:float, ts:float, n_estimat:int, max_dep:int, rand_state:int) :
    """ Build a Random Forest Classifier with the data and hyper parameters given

    Args:
        data (:obj:`DataFrame <pandas.DataFrame>`): a dataframe of the cloud data
        target_colname (str): the name of the "target" column; default is "target"
            (specified in config.yaml)
        sample_strat (float): "sampling_strategy" argument for oversampling the minor class
        ts (float): "test_size" argument for train test split;
            default is 0.4 (specified in config.yaml)
        n_estimat (int): "n_estimators" argument for random forest classifier;
            default is 10 (specified in config.yaml)
        max_dep (int): "max_depth" argument for random forest classifier;
            default is 10 (specified in config.yaml)
        rand_state (int): set "random_state" to ensure reproducibility;
            default is 0 (specified in config.yaml)

    Returns:
        [rf, X_test, y_test, X_train, y_train] (:obj:`list`): the first object in the list is
            the random forest classifier model trained; the second object
            in the list is the X_test (the test DataFrame to generate predictions on);
            the third object in the list is the y_test (the result series that
            we are classifying (target))

    """
    features = data.drop([target_colname], axis=1)

    target = data[[target_colname]].values.ravel()
    logger.info('Target column length: %s', len(features.columns))
    logger.info('Target column name: %s', target_colname)
    logger.info('Major class initial count: %i', target[target == 1].shape[0])
    logger.info('Minor class initial count: %i', target[target == 0].shape[0])

    # define oversampling strategy
    oversample = RandomOverSampler(sampling_strategy=sample_strat, random_state=rand_state)

    # fit and apply the transform
    X_over, y_over = oversample.fit_resample(features, target)
    logger.info('Minor class oversampled count: %i', y_over[y_over == 0].shape[0])

    # train test split
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X_over,
                                                                                y_over,
                                                                                test_size=ts,
                                                                   random_state=rand_state)
    y_train=pd.DataFrame(y_train,columns=[target_colname])      
    y_test=pd.DataFrame(y_test,columns=[target_colname])
    x_names = X_train.columns
    X_test=X_test.reset_index(drop=True)
    X_train=X_train.reset_index(drop=True)
    # random forest model
    rf = sklearn.ensemble.RandomForestClassifier(n_estimators=n_estimat,
                                                 max_depth=max_dep,
                                                 random_state=rand_state)
    rf.fit(X_train[x_names], y_train)
    logger.info('Random Forest Classifier successfully trained')
    
   
    return rf, y_test, y_train,X_test,X_train


