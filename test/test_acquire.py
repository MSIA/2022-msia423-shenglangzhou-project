"""
Test acquire.py module
"""
import pytest

import pandas as pd
import numpy as np

from src.acquire import filna, clean_column, neg_to_pos, replace_cat


def test_filna():
    """test1 (filna()): happy path for expected behavior"""
    # Define input DataFrame
    df_in_values = [[0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [0.],
                    [np.nan],
                    [0.],
                    [np.nan],
                    [0.],
                    [0.],
                    [0.]]
    df_in_index = [64282, 94645, 306349, 258314, 87597, 27731, 284391, 267734,
                   238789, 299374, 188398, 252746, 249037, 294226, 91317, 219832,
                   70781, 1710, 195776, 143511]
    df_in_columns = ['Age']
    val=0

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0],
         [0.0]],
        index=[64282, 94645, 306349, 258314, 87597, 27731, 284391, 267734,
               238789, 299374, 188398, 252746, 249037, 294226, 91317, 219832,
               70781, 1710, 195776, 143511],
        columns=['Age'])

    # Compute test output
    df_test = filna(df_in, 'Age',0)

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_filna_non_df():
    """test2 (filna()): unhappy path when dataframe is not provided"""
    df_in = 'I am not a DataFrame'

    with pytest.raises(TypeError):
        filna(df_in, 'amt_req_credit_bureau_day')


def test_clean_column():
    """test3 (clean_column()): happy path for expected behavior"""
    # Define input DataFrame
    df_in_values = [['Secondary / secondary special'],
                    ['Secondary / secondary special'],
                    ['Secondary / secondary special'],
                    ['Incomplete higher'],
                    ['Secondary / secondary special'],
                    ['Secondary / secondary special'],
                    ['Secondary / secondary special'],
                    ['Higher education'],
                    ['Secondary / secondary special'],
                    ['Secondary / secondary special'],
                    ['Secondary / secondary special'],
                    ['Secondary / secondary special'],
                    ['Higher education'],
                    ['Secondary / secondary special'],
                    ['Higher education'],
                    ['Higher education'],
                    ['Higher education'],
                    ['Secondary / secondary special'],
                    ['Lower secondary'],
                    ['Higher education']]
    df_in_index = [64282, 94645, 306349, 258314, 87597, 27731, 284391, 267734,
                   238789, 299374, 188398, 252746, 249037, 294226, 91317, 219832,
                   70781, 1710, 195776, 143511]
    df_in_columns = ['NAME_EDUCATION_TYPE']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [['Secondary education'],
         ['Secondary education'],
         ['Secondary education'],
         ['Incomplete higher'],
         ['Secondary education'],
         ['Secondary education'],
         ['Secondary education'],
         ['Higher education'],
         ['Secondary education'],
         ['Secondary education'],
         ['Secondary education'],
         ['Secondary education'],
         ['Higher education'],
         ['Secondary education'],
         ['Higher education'],
         ['Higher education'],
         ['Higher education'],
         ['Secondary education'],
         ['Secondary education'],
         ['Higher education']],
        index=[64282, 94645, 306349, 258314, 87597, 27731, 284391, 267734,
               238789, 299374, 188398, 252746, 249037, 294226, 91317, 219832,
               70781, 1710, 195776, 143511],
        columns=['NAME_EDUCATION_TYPE'])

    # Compute test output
    edu_replace_dict = dict({'Secondary / secondary special': 'Secondary education',
                             'Lower secondary': 'Secondary education',
                             'Academic degree': 'Higher education'})
    df_test = clean_column(df_in, 'NAME_EDUCATION_TYPE', edu_replace_dict)

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_clean_column_non_df():
    """test4 (clean_column()): unhappy path when dataframe is not provided"""
    df_in = 'I am not a DataFrame'
    edu_replace_dict = dict({'Secondary / secondary special': 'Secondary education',
                             'Lower secondary': 'Secondary education',
                             'Academic degree': 'Higher education'})

    with pytest.raises(TypeError):
        clean_column(df_in, 'NAME_EDUCATION_TYPE', edu_replace_dict)


def test_neg_to_pos():
    """test5 (neg_to_pos()): happy path for expected behavior"""
    # Define input DataFrame
    df_in_values = [[-20614, 365243, -3098],
                    [-9080, -1080, -1743],
                    [-15933, -114, -4424],
                    [-9926, -1061, -2474],
                    [-11757, -1593, -81],
                    [-22402, 365243, -4216],
                    [-18576, -4725, -2026],
                    [-14783, -84, -2537],
                    [-16032, -5139, -4019],
                    [-18445, -10811, -1988],
                    [-16012, -1089, -4191],
                    [-20600, 365243, -3555],
                    [-13622, -810, -4366],
                    [-11361, -526, -3970],
                    [-15234, -858, -4756],
                    [-9498, -410, -2155],
                    [-8683, -773, -1342],
                    [-12589, -2085, -3666],
                    [-18235, -3729, -1762],
                    [-10147, -562, -529]]
    df_in_index = [64282, 94645, 306349, 258314, 87597, 27731, 284391, 267734,
                   238789, 299374, 188398, 252746, 249037, 294226, 91317, 219832,
                   70781, 1710, 195776, 143511]
    df_in_columns = ['days_birth', 'days_employed', 'days_id_change']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[20614, -365243, 3098],
         [9080, 1080, 1743],
         [15933, 114, 4424],
         [9926, 1061, 2474],
         [11757, 1593, 81],
         [22402, -365243, 4216],
         [18576, 4725, 2026],
         [14783, 84, 2537],
         [16032, 5139, 4019],
         [18445, 10811, 1988],
         [16012, 1089, 4191],
         [20600, -365243, 3555],
         [13622, 810, 4366],
         [11361, 526, 3970],
         [15234, 858, 4756],
         [9498, 410, 2155],
         [8683, 773, 1342],
         [12589, 2085, 3666],
         [18235, 3729, 1762],
         [10147, 562, 529]],
        index=[64282, 94645, 306349, 258314, 87597, 27731, 284391, 267734,
               238789, 299374, 188398, 252746, 249037, 294226, 91317, 219832,
               70781, 1710, 195776, 143511],
        columns=['days_birth', 'days_employed', 'days_id_change'])

    # Compute test output
    df_test = neg_to_pos(df_in, ['days_birth', 'days_employed', 'days_id_change'])

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_neg_to_pos_non_df():
    """test6 (neg_to_pos()): unhappy path when dataframe is not provided"""
    df_in = 'I am not a DataFrame'

    with pytest.raises(TypeError):
        neg_to_pos(df_in, ['days_birth', 'days_employed', 'days_id_change'])


def test_replace_cat():
    """test7 (replace_cat()): happy path for expected behavior"""
    # Define input DataFrame
    df_in_values = [['N', 'Y', '1', 'F'],
                    ['Y', 'Y', '1', 'M'],
                    ['Y', 'Y', '1', 'M'],
                    ['Y', 'N', '1', 'M'],
                    ['N', 'Y', '1', 'M'],
                    ['N', 'Y', '1', 'F'],
                    ['N', 'N', '1', 'F'],
                    ['N', 'N', '1', 'F'],
                    ['N', 'N', '1', 'F'],
                    ['Y', 'N', '1', 'M'],
                    ['N', 'Y', '1', 'F'],
                    ['Y', 'Y', '1', 'F'],
                    ['N', 'N', '1', 'M'],
                    ['Y', 'Y', '1', 'M'],
                    ['Y', 'N', '1', 'M'],
                    ['Y', 'Y', '1', 'F'],
                    ['N', 'Y', '1', 'F'],
                    ['N', 'Y', '1', 'F'],
                    ['Y', 'N', '1', 'M'],
                    ['N', 'N', '1', 'F']]
    df_in_index = [64282, 94645, 306349, 258314, 87597, 27731, 284391, 267734,
                   238789, 299374, 188398, 252746, 249037, 294226, 91317, 219832,
                   70781, 1710, 195776, 143511]
    df_in_columns = ['FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'FLAG_MOBIL', 'CODE_GENDER']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [['No', 'Yes', 'Yes', 'Female'],
         ['Yes', 'Yes', 'Yes', 'Male'],
         ['Yes', 'Yes', 'Yes', 'Male'],
         ['Yes', 'No', 'Yes', 'Male'],
         ['No', 'Yes', 'Yes', 'Male'],
         ['No', 'Yes', 'Yes', 'Female'],
         ['No', 'No', 'Yes', 'Female'],
         ['No', 'No', 'Yes', 'Female'],
         ['No', 'No', 'Yes', 'Female'],
         ['Yes', 'No', 'Yes', 'Male'],
         ['No', 'Yes', 'Yes', 'Female'],
         ['Yes', 'Yes', 'Yes', 'Female'],
         ['No', 'No', 'Yes', 'Male'],
         ['Yes', 'Yes', 'Yes', 'Male'],
         ['Yes', 'No', 'Yes', 'Male'],
         ['Yes', 'Yes', 'Yes', 'Female'],
         ['No', 'Yes', 'Yes', 'Female'],
         ['No', 'Yes', 'Yes', 'Female'],
         ['Yes', 'No', 'Yes', 'Male'],
         ['No', 'No', 'Yes', 'Female']],
        index=[64282, 94645, 306349, 258314, 87597, 27731, 284391, 267734,
               238789, 299374, 188398, 252746, 249037, 294226, 91317, 219832,
               70781, 1710, 195776, 143511],
        columns=['FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'FLAG_MOBIL', 'CODE_GENDER'])

    # Compute test output
    cat_dict = {'FLAG_OWN_CAR': {"Y": "Yes", "N": "No"},
                'FLAG_OWN_REALTY': {"Y": "Yes", "N": "No"},
                'FLAG_MOBIL': {"1": "Yes", "0": "No"},
                'CODE_GENDER': {"M": "Male", "F": "Female"}}
    df_test = replace_cat(df_in, cat_dict)

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_replace_cat_non_df():
    """test8 (replace_cat()): unhappy path when dataframe is not provided"""
    df_in = 'I am not a DataFrame'
    cat_dict = {'FLAG_OWN_CAR': {"Y": "Yes", "N": "No"},
                'FLAG_OWN_REALTY': {"Y": "Yes", "N": "No"},
                'FLAG_MOBIL': {"1": "Yes", "0": "No"},
                'CODE_GENDER': {"M": "Male", "F": "Female"}}

    with pytest.raises(TypeError):
        replace_cat(df_in, cat_dict)
