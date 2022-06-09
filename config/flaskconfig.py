import os
from xmlrpc.client import Boolean

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "credit_card_application"
SQLALCHEMY_Application_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

# Connection string
DB_HOST = os.environ.get('MYSQL_HOST')
DB_PORT = os.environ.get('MYSQL_PORT')
DB_USER = os.environ.get('MYSQL_USER')
DB_PW = os.environ.get('MYSQL_PASSWORD')
DATABASE = os.environ.get('DATABASE_NAME')
DB_DIALECT = 'mysql+pymysql'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
S3_BUCKET = os.environ.get('S3_BUCKET')
if SQLALCHEMY_DATABASE_URI is not None:
    pass
elif DB_HOST is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/application.db'
else:
    SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{pw}@{host}:{port}/{db}'.format(dialect=DB_DIALECT, user=DB_USER,
                                                                                  pw=DB_PW, host=DB_HOST, port=DB_PORT,
                                                                                  db=DATABASE)

# Categorical questions used in the app

GENDERS = ['Male', 'Female']
BINARY = ['Y', 'N']
BOOL = ['Yes','No']
INCOME_TYPE = ['Working', 'State servant', 'Commercial associate', 'Pensioner',
                'Student']
EDU_TYPE = ['Secondary education', 'Incomplete higher', 'Higher education']
FAM_STATUS = ['Single / not married', 'Married', 'Civil marriage', 'Widow', 'Separated']
HOUSING_TYPE = ['Rented apartment', 'House / apartment', 'With parents', 'Municipal apartment', 'Office apartment']
OCCUPATION_TYPE = ['Sales staff', 'Core staff', 'Laborers','Managers', 'Drivers', 'Not Specified', 'Cooking staff', 'HR staff','High skill tech staff','Low-skill Laborers', 'Medicine staff']