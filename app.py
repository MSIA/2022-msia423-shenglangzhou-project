"""
This file defines some functionality in the app
"""

import traceback
import logging.config

import yaml
from flask import Flask
from flask import render_template, request

from config.flaskconfig import GENDERS, BINARY, INCOME_TYPE, EDU_TYPE, FAM_STATUS, HOUSING_TYPE,OCCUPATION_TYPE,BOOL
from src.add_application import ApplicationManager
from src.predict import transform_input, get_prediction

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
application_manager = ApplicationManager(app)

# load yaml configuration file
try:
    with open('config/config.yaml', "r") as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
        logger.info("Configuration file loaded")
except FileNotFoundError:
    logger.error("Configuration file is not found")


@app.route('/')
def index():
    """Main view of the loan application that allows user input applicant information

    Create view into index page that allows users input applicant information

    Returns:
        rendered html template located at: app/templates/index.html

    """

    try:
        logger.debug("Index page accessed")
        return render_template('index.html', genders=GENDERS, own_car=BOOL, own_realty=BOOL,income_type=INCOME_TYPE, edu_type=EDU_TYPE, fam_status=FAM_STATUS, housing_type=HOUSING_TYPE, occupation_type=OCCUPATION_TYPE, own_mobil=BOOL,own_work_phone=BOOL,own_phone=BOOL, own_email=BOOL, employed=BOOL)
    except:
        traceback.print_exc()
        logger.warning("Not able to display loan applications information, error page returned")
        return render_template('error.html')


@app.route('/result', methods=['POST', 'GET'])
def add_entry():
    """View that process a POST with new applicant input

    Add new applicant information to Applications database and get prediction results

    Returns:
        rendered html template located at: app/templates/result.html if successfully processed,
        rendered html template located at: app/templates/error.html if any error occurs

    """
    if request.method == 'GET':
        return "Visit the homepage to add applicants and get predictions"
    elif request.method == 'POST':
        # try:
        # Add new applicant information to RDS for future usages
        application_manager.add_application(
            CODE_GENDER=request.form['gender'],
            FLAG_OWN_CAR=request.form['own_car'],
            FLAG_OWN_REALTY=request.form['own_realty'],
            CNT_CHILDREN=request.form['num_children'],
            AMT_INCOME_TOTAL=request.form['income_total'],
            NAME_INCOME_TYPE=request.form['income_type'],
            NAME_EDUCATION_TYPE=request.form['edu_type'],
            NAME_FAMILY_STATUS=request.form['family_status'],
            NAME_HOUSING_TYPE=request.form['housing_type'],
            AGE=request.form['years_birth'],
            YEARS_EMPLOYED=request.form['years_employed'],
            FLAG_MOBIL=request.form['own_mobil'],
            FLAG_WORK_PHONE=request.form['own_work_phone'],
            FLAG_PHONE=request.form['own_phone'],
            FLAG_EMAIL=request.form['own_email'],
            OCCUPATION_TYPE=request.form['occupation_type'],
            CNT_FAM_MEMBERS=request.form['cnt_family_members'],
            EMPLOYED=request.form['employed']
        )

        logger.info(
            "New applicant %s added"
        )

        # Get loan delinquency prediction for the new applicant
        user_input = {
            'CODE_GENDER':request.form['gender'],
            'FLAG_OWN_CAR':request.form['own_car'],
            'FLAG_OWN_REALTY':request.form['own_realty'],
            'CNT_CHILDREN':request.form['num_children'],
            'AMT_INCOME_TOTAL':request.form['income_total'],
            'NAME_INCOME_TYPE':request.form['income_type'],
            'NAME_EDUCATION_TYPE':request.form['edu_type'],
            'NAME_FAMILY_STATUS':request.form['family_status'],
            'NAME_HOUSING_TYPE':request.form['housing_type'],
            'AGE':request.form['years_birth'],
            'YEARS_EMPLOYED':request.form['years_employed'],
            'FLAG_MOBIL':request.form['own_mobil'],
            'FLAG_WORK_PHONE':request.form['own_work_phone'],
            'FLAG_PHONE':request.form['own_phone'],
            'FLAG_EMAIL':request.form['own_email'],
            'OCCUPATION_TYPE':request.form['occupation_type'],
            'CNT_FAM_MEMBERS':request.form['cnt_family_members'],
            'EMPLOYED':request.form['employed']
            }
        user_input_transformed = transform_input(user_input,
                                                    **conf['predict']['transform_input'])
        print(user_input_transformed)                                           
        user_prob = get_prediction(user_input_transformed,
                                    **conf['predict']['get_prediction'])[0]
        user_bin = get_prediction(user_input_transformed,
                                    **conf['predict']['get_prediction'])[1]

        logger.info(
            "The new applicant's probability of loan delinquency is: %f percent, "
            "hence %s", user_prob, user_bin
        )

        logger.debug("Result page accessed")
        return render_template('result.html', user_prob=user_prob, user_bin=user_bin)
    # except:
    #     logger.warning("Not able to process your request, error page returned")
    #     return render_template('error.html')


@app.route('/about', methods=['GET'])
def about():
    """View of an 'About' page that has detailed information about the project

    Returns:
        rendered html template located at: app/templates/about.html

    """
    logger.debug("About page accessed")
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
