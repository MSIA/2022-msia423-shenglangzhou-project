"""
Test predict.py module
"""
import pytest

import pandas as pd

from src.predict import transform_input


def test_transform_input():
    """test1 (transform_input()): happy path for expected behavior"""
    # Define input DataFrame
    sample_input = {'contract_type': "Cash Loans", 'gender': "Female", 'own_car': "Yes",
                    'own_realty': "Yes", 'num_children': 0, 'income_total': 200000,
                    'amt_credit': 10000, 'amt_annuity': 14000,
                    'amt_goods_price': 30000, 'income_type': 'Working',
                    'edu_type': 'Secondary education', 'family_status': 'Single / not married',
                    'Age': 23, 'Years_Employed': 2, 'Years_ID_Publish': 10,
                    'phone_contactable': "Yes", 'cnt_family_members': 4,
                    'amt_req_credit_bureau_day': 0, 'Employed': "No"}

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[0.0, 200000.0, 10000.0, 14000.0, 30000.0, 23.0, 2.0, 10.0, 4.0,
          0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
          0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0]],
        index=[0],
        columns=['num_children', 'income_total', 'amt_credit', 'amt_annuity',
                 'amt_goods_price', 'Age', 'Years_Employed', 'Years_ID_Publish',
                 'cnt_family_members', 'amt_req_credit_bureau_day',
                 'contract_type_Revolving loans', 'gender_Male', 'gender_Not Provided',
                 'own_car_Yes', 'own_reality_Yes', 'income_type_Commercial associate',
                 'income_type_Maternity leave', 'income_type_Pensioner',
                 'income_type_State servant', 'income_type_Student',
                 'income_type_Unemployed', 'income_type_Working',
                 'edu_type_Incomplete higher', 'edu_type_Secondary education',
                 'family_status_Married', 'family_status_Separated',
                 'family_status_Single / not married', 'family_status_Widow',
                 'phone_contactable_Yes', 'Employed_Yes'])

    # Compute test output
    col_li = ['contract_type', 'gender', 'own_car', 'own_realty', 'income_type',
              'edu_type', 'family_status', 'phone_contactable', 'Employed']
    ohe_cols = ['num_children', 'income_total', 'amt_credit', 'amt_annuity',
                'amt_goods_price', 'Age', 'Years_Employed', 'Years_ID_Publish',
                'cnt_family_members', 'amt_req_credit_bureau_day',
                'contract_type_Revolving loans', 'gender_Male',
                'gender_Not Provided', 'own_car_Yes',
                'own_reality_Yes', 'income_type_Commercial associate',
                'income_type_Maternity leave', 'income_type_Pensioner',
                'income_type_State servant', 'income_type_Student',
                'income_type_Unemployed', 'income_type_Working',
                'edu_type_Incomplete higher', 'edu_type_Secondary education',
                'family_status_Married', 'family_status_Separated',
                'family_status_Single / not married', 'family_status_Widow',
                'phone_contactable_Yes', 'Employed_Yes']
    df_test = transform_input(sample_input, col_li, ohe_cols)
    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_transform_input_non_dict():
    """test2 (transform_input()): unhappy path when dataframe is not provided"""
    sample_input = 'I am not a dictionary'

    col_li = ['contract_type', 'gender', 'own_car', 'own_realty', 'income_type',
              'edu_type', 'family_status', 'phone_contactable', 'Employed']
    ohe_cols = ['num_children', 'income_total', 'amt_credit', 'amt_annuity',
                'amt_goods_price', 'Age', 'Years_Employed', 'Years_ID_Publish',
                'cnt_family_members', 'amt_req_credit_bureau_day',
                'contract_type_Revolving loans', 'gender_Male',
                'gender_Not Provided', 'own_car_Yes',
                'own_reality_Yes', 'income_type_Commercial associate',
                'income_type_Maternity leave', 'income_type_Pensioner',
                'income_type_State servant', 'income_type_Student',
                'income_type_Unemployed', 'income_type_Working',
                'edu_type_Incomplete higher', 'edu_type_Secondary education',
                'family_status_Married', 'family_status_Separated',
                'family_status_Single / not married', 'family_status_Widow',
                'phone_contactable_Yes', 'Employed_Yes']

    with pytest.raises(ValueError):
        transform_input(sample_input, col_li, ohe_cols)
