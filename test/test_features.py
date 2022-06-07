"""
Test features.py module
"""
import pytest

import pandas as pd
import numpy as np

from src.features import day_to_year, create_new_col, get_ohe_data


def test_day_to_year():
    """test1 (day_to_year()): happy path for expected behavior"""
    # Define input DataFrame
    df_in_values = [[16836, 7908, 374],
                    [23137, -365243, 3943],
                    [13094, 4468, 4044],
                    [21092, -365243, 4638],
                    [14677, 3806, 2563],
                    [10355, 2102, 3004],
                    [23836, -365243, 4051],
                    [8820, 834, 1479],
                    [16691, 978, 241],
                    [11248, 1561, 3331],
                    [11018, 4402, 3408],
                    [21595, -365243, 1432],
                    [15771, 3086, 4999],
                    [17038, 2019, 570],
                    [16101, 7141, 4452],
                    [15806, 378, 2420],
                    [22912, -365243, 4194],
                    [15196, 2256, 4396],
                    [15723, 3166, 2540],
                    [21866, -365243, 4294]]
    df_in_index = [293459, 273633, 47968, 59177, 305435, 94319, 137097, 285926,
                   303668, 209739, 67537, 60363, 168212, 81346, 52494, 253940,
                   218425, 260186, 177850, 140020]
    df_in_columns = ['days_birth', 'days_employed', 'days_id_change']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[16836, 7908, 374, 46.0, 22.0, 1.0],
         [23137, -365243, 3943, 63.0, -1001.0, 11.0],
         [13094, 4468, 4044, 36.0, 12.0, 11.0],
         [21092, -365243, 4638, 58.0, -1001.0, 13.0],
         [14677, 3806, 2563, 40.0, 10.0, 7.0],
         [10355, 2102, 3004, 28.0, 6.0, 8.0],
         [23836, -365243, 4051, 65.0, -1001.0, 11.0],
         [8820, 834, 1479, 24.0, 2.0, 4.0],
         [16691, 978, 241, 46.0, 3.0, 1.0],
         [11248, 1561, 3331, 31.0, 4.0, 9.0],
         [11018, 4402, 3408, 30.0, 12.0, 9.0],
         [21595, -365243, 1432, 59.0, -1001.0, 4.0],
         [15771, 3086, 4999, 43.0, 8.0, 14.0],
         [17038, 2019, 570, 47.0, 6.0, 2.0],
         [16101, 7141, 4452, 44.0, 20.0, 12.0],
         [15806, 378, 2420, 43.0, 1.0, 7.0],
         [22912, -365243, 4194, 63.0, -1001.0, 11.0],
         [15196, 2256, 4396, 42.0, 6.0, 12.0],
         [15723, 3166, 2540, 43.0, 9.0, 7.0],
         [21866, -365243, 4294, 60.0, -1001.0, 12.0]],
        index=[293459, 273633, 47968, 59177, 305435, 94319, 137097, 285926,
               303668, 209739, 67537, 60363, 168212, 81346, 52494, 253940,
               218425, 260186, 177850, 140020],
        columns=['days_birth', 'days_employed', 'days_id_change', 'Age',
                 'Years_Employed', 'Years_ID_Publish'])

    # Compute test output
    new_cols_dict = {'Age': 'days_birth',
                     'Years_Employed': 'days_employed',
                     'Years_ID_Publish': 'days_id_change'}
    df_test = day_to_year(df_in, new_cols_dict)

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_day_to_year_non_df():
    """test2 (day_to_year()): unhappy path when dataframe is not provided"""
    df_in = 'I am not a DataFrame'
    new_cols_dict = {'Age': 'days_birth',
                     'Years_Employed': 'days_employed',
                     'Years_ID_Publish': 'days_id_change'}

    with pytest.raises(TypeError):
        day_to_year(df_in, new_cols_dict)


def test_create_new_col():
    """test3 (create_new_col()): happy path for expected behavior"""
    # Define input DataFrame
    df_in_values = [[7908],
                    [-365243],
                    [4468],
                    [-365243],
                    [3806],
                    [2102],
                    [-365243],
                    [834],
                    [978],
                    [1561],
                    [4402],
                    [-365243],
                    [3086],
                    [2019],
                    [7141],
                    [378],
                    [-365243],
                    [2256],
                    [3166],
                    [-365243]]
    df_in_index = [293459, 273633, 47968, 59177, 305435, 94319, 137097, 285926,
                   303668, 209739, 67537, 60363, 168212, 81346, 52494, 253940,
                   218425, 260186, 177850, 140020]
    df_in_columns = ['days_employed']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[7908, 'Yes'],
         [-365243, 'No'],
         [4468, 'Yes'],
         [-365243, 'No'],
         [3806, 'Yes'],
         [2102, 'Yes'],
         [-365243, 'No'],
         [834, 'Yes'],
         [978, 'Yes'],
         [1561, 'Yes'],
         [4402, 'Yes'],
         [-365243, 'No'],
         [3086, 'Yes'],
         [2019, 'Yes'],
         [7141, 'Yes'],
         [378, 'Yes'],
         [-365243, 'No'],
         [2256, 'Yes'],
         [3166, 'Yes'],
         [-365243, 'No']],
        index=[293459, 273633, 47968, 59177, 305435, 94319, 137097, 285926,
               303668, 209739, 67537, 60363, 168212, 81346, 52494, 253940,
               218425, 260186, 177850, 140020],
        columns=['days_employed', 'Employed'])

    # Compute test output
    df_test = create_new_col(df_in, 'days_employed', 'Employed')

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_create_new_col_non_df():
    """test4 (create_new_col()): unhappy path when dataframe is not provided"""
    df_in = 'I am not a DataFrame'

    with pytest.raises(TypeError):
        create_new_col(df_in, 'days_employed', 'Employed')


def test_get_ohe_data():
    """test5 (get_ohe_data()): happy path for expected behavior"""
    # Define input DataFrame
    df_in_values = [['Cash loans', 'Female', 'No', 'Yes', 'Working', 'Higher education', 'Married',
                     'Yes', 'Yes', 0, 540000.0, 785398.5, 34726.5, 702000.0, 46.0, 22.0,
                     1.0, 2.0, 0.0, 0],
                    ['Cash loans', 'Female', 'No', 'No', 'Pensioner', 'Secondary education',
                     'Married', 'Yes', 'No', 0, 157500.0, 396171.0, 28305.0, 342000.0, 63.0,
                     -1001.0, 11.0, 2.0, 0.0, 0],
                    ['Cash loans', 'Male', 'No', 'Yes', 'State servant', 'Higher education',
                     'Married', 'Yes', 'Yes', 1, 247500.0, 675000.0, 26901.0, 675000.0,
                     36.0, 12.0, 11.0, 3.0, 0.0, 0],
                    ['Cash loans', 'Female', 'No', 'Yes', 'Pensioner', 'Secondary education',
                     'Married', 'Yes', 'No', 0, 540000.0, 1325475.0, 56160.0, 1125000.0,
                     58.0, -1001.0, 13.0, 2.0, 0.0, 0],
                    ['Cash loans', 'Male', 'Yes', 'Yes', 'Working', 'Secondary education',
                     'Civil marriage', 'Yes', 'Yes', 0, 180000.0, 720000.0, 21051.0,
                     720000.0, 40.0, 10.0, 7.0, 2.0, 0.0, 0]]
    df_in_index = [293459, 273633, 47968, 59177, 305435]
    df_in_columns = ['contract_type', 'gender', 'own_car', 'own_realty', 'income_type',
                     'edu_type', 'family_status', 'phone_contactable', 'Employed',
                     'num_children', 'income_total', 'amt_credit', 'amt_annuity',
                     'amt_goods_price', 'Age', 'Years_Employed', 'Years_ID_Publish',
                     'cnt_family_members', 'amt_req_credit_bureau_day', 'target']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[0, 540000.0, 785398.5, 34726.5, 702000.0, 46.0, 22.0, 1.0, 2.0,
          0.0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
         [0, 157500.0, 396171.0, 28305.0, 342000.0, 63.0, -1001.0, 11.0,
          2.0, 0.0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
         [1, 247500.0, 675000.0, 26901.0, 675000.0, 36.0, 12.0, 11.0,
          3.0, 0.0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
         [0, 540000.0, 1325475.0, 56160.0, 1125000.0, 58.0, -1001.0,
          13.0, 2.0, 0.0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
         [0, 180000.0, 720000.0, 21051.0, 720000.0, 40.0, 10.0, 7.0, 2.0,
          0.0, 0, 1, 1, 1, 0, 1, 1, 0, 1]],
        index=[293459, 273633, 47968, 59177, 305435],
        columns=['num_children', 'income_total', 'amt_credit', 'amt_annuity',
                 'amt_goods_price', 'Age', 'Years_Employed', 'Years_ID_Publish',
                 'cnt_family_members', 'amt_req_credit_bureau_day', 'target',
                 'gender_Male', 'own_car_Yes', 'own_realty_Yes',
                 'income_type_State servant', 'income_type_Working',
                 'edu_type_Secondary education', 'family_status_Married',
                 'Employed_Yes'])
    df_true.iloc[:, -8:] = df_true.iloc[:, -8:].astype(np.uint8)

    # Compute test output
    cat_vars = ['contract_type', 'gender',
                'own_car', 'own_realty',
                'income_type', 'edu_type',
                'family_status', 'phone_contactable',
                'Employed']
    num_vars = ['num_children', 'income_total', 'amt_credit',
                'amt_annuity', 'amt_goods_price', 'Age',
                'Years_Employed', 'Years_ID_Publish', 'cnt_family_members',
                'amt_req_credit_bureau_day']
    df_test = get_ohe_data(df_in, cat_vars, num_vars, 'target')

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_get_ohe_data_non_df():
    """test6 (get_ohe_data()): unhappy path when dataframe is not provided"""
    df_in = 'I am not a DataFrame'

    cat_vars = ['contract_type', 'gender',
                'own_car', 'own_realty',
                'income_type', 'edu_type',
                'family_status', 'phone_contactable',
                'Employed']
    num_vars = ['num_children', 'income_total', 'amt_credit',
                'amt_annuity', 'amt_goods_price', 'Age',
                'Years_Employed', 'Years_ID_Publish', 'cnt_family_members',
                'amt_req_credit_bureau_day']

    with pytest.raises(TypeError):
        get_ohe_data(df_in, cat_vars, num_vars, 'target')
