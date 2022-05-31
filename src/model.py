"""
This module contains multiple functions that offers
model training and model evaluation functionality
"""
import logging

import pandas as pd
import sklearn
import sklearn.ensemble
from imblearn.over_sampling import RandomOverSampler

logger = logging.getLogger(__name__)


def train_model(data, target_colname, sample_strat, ts, n_estimat, max_dep, rand_state):
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
        [rf, X_test, y_test] (:obj:`list`): the first object in the list is
            the random forest classifier model trained; the second object
            in the list is the X_test (the test DataFrame to generate predictions on);
            the third object in the list is the y_test (the result series that
            we are classifying (target))

    """
    features = data.drop([target_colname], axis=1)
    target = data[[target_colname]].values.ravel()
    logger.info('Target column name: %s', target_colname)
    logger.info('Minor class initial count: %i', target[target == 1].shape[0])
    logger.info('Major class initial count: %i', target[target == 0].shape[0])

    # define oversampling strategy
    oversample = RandomOverSampler(sampling_strategy=sample_strat, random_state=rand_state)

    # fit and apply the transform
    X_over, y_over = oversample.fit_resample(features, target)
    logger.info('Minor class oversampled count: %i', y_over[y_over == 1].shape[0])

    # train test split
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X_over,
                                                                                y_over,
                                                                                test_size=ts,
                                                                                random_state=rand_state)
    x_names = X_train.columns

    # random forest model
    rf = sklearn.ensemble.RandomForestClassifier(n_estimators=n_estimat,
                                                 max_depth=max_dep,
                                                 random_state=rand_state)
    rf.fit(X_train[x_names], y_train)
    logger.info('Random Forest Classifier successfully trained')
    return [rf, X_test, y_test]


def evaluate(rf_model, X_test, y_test, save_path):
    """ Score the random forest model and evaluate the model performance

    Args:
        rf_model (:obj:`RandomForestClassifier`): trained random forest model object
        X_test(:obj:`DataFrame <pandas.DataFrame>`): the test dataframe to generate predictions on
        y_test(:obj:`Series <pandas.Series>`): the result series that we are classifying (target)

    Returns:
        None

    """
    # predict probability and class for each sample in the test set
    x_names = X_test.columns
    ypred_proba_test = rf_model.predict_proba(X_test[x_names])[:, 1]
    ypred_bin_test = rf_model.predict(X_test[x_names])

    # calculate metrics
    test_auc = sklearn.metrics.roc_auc_score(y_test, ypred_proba_test)

    test_acc = sklearn.metrics.accuracy_score(y_test, ypred_bin_test)

    logger.info('Completed evaluation of the Random Forest Classifier')
    logger.info('AUC on test: %0.3f', test_auc)
    logger.info('Accuracy on test: %0.3f', test_acc)

    try:
        eval_result = pd.DataFrame({"AUC": test_auc, "ACC": test_acc}, index=[0])
        eval_result.to_csv(save_path, index=False)
        logger.info("Evaluation results saved to location: %s", save_path)
    except ValueError:
        logger.error("Failed to save the evaluation results because "
                     "the DataFrame of evaluation results cannot be appropriately called")
