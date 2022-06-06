"""
This file contains multiple functions that offers
creating database and adding new data to the database functionality
"""
import logging.config

import pandas as pd
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger(__name__)

Base = declarative_base()


class Application(Base):
    """Create a data model for the database for capturing loan applicants information"""

    __tablename__ = 'applications'

    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,autoincrement=True)
    CODE_GENDER  = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    FLAG_OWN_CAR = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    FLAG_OWN_REALTY= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    CNT_CHILDREN= sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    AMT_INCOME_TOTAL= sqlalchemy.Column(sqlalchemy.Float, unique=False, nullable=True)
    NAME_INCOME_TYPE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    NAME_EDUCATION_TYPE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    NAME_FAMILY_STATUS= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    NAME_HOUSING_TYPE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    AGE= sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    YEARS_EMPLOYED= sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    FLAG_MOBIL= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    FLAG_WORK_PHONE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    FLAG_PHONE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    FLAG_EMAIL= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    OCCUPATION_TYPE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True) 
    CNT_FAM_MEMBERS= sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True) 
    EMPLOYED = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    def __repr__(self):
        return '<Application ID %r>' % self.id


def create_db(engine_string: str):
    """Create a database from provided engine string

    Args:
        engine_string (str): Engine string

    Returns:
        None

    """
    try:
        engine = sqlalchemy.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database created at %s", engine_string)
    except sqlalchemy.exc.ArgumentError:
        logger.error('%s is not a valid engine string', engine_string)
    except sqlalchemy.exc.OperationalError:
        logger.error('Failed to connect to server. '
                     'Please check if you are connected to Northwestern VPN')


class ApplicationManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app (Flask): Flask app
            engine_string (str): Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self):
        """Closes SQLAlchemy session

        Returns:
            None

        """
        self.session.close()

    def add_application(self, CODE_GENDER:str,
                FLAG_OWN_CAR:str,
                FLAG_OWN_REALTY:str,
                CNT_CHILDREN:int,
                AMT_INCOME_TOTAL:float,
                NAME_INCOME_TYPE:str,
                NAME_EDUCATION_TYPE:str,
                NAME_FAMILY_STATUS:str,
                NAME_HOUSING_TYPE:str,
                AGE:int,
                YEARS_EMPLOYED:int,
                FLAG_MOBIL:str,
                FLAG_WORK_PHONE:str,
                FLAG_PHONE:str,
                FLAG_EMAIL:str,
                OCCUPATION_TYPE:str,
                CNT_FAM_MEMBERS:int,
                EMPLOYED:str):
        """Seeds an existing database with additional applications.

        Args:
            CODE_GENDER(str): Gender of the client
            FLAG_OWN_CAR(str): Flag if the client owns a car
            FLAG_OWN_REALTY(str): Flag if client owns a house or flat
            CNT_CHILDREN (int): Number of children the client has
            AMT_INCOME_TOTAL (float): Income of the client
            amt_goods_price (float): price of the goods for which the loan is given
            NAME_INCOME_TYPE (str): Clients income type
            NAME_EDUCATION_TYPE(str): Level of highest education the client achieved
            NAME_FAMILY_STATUS (str): Family status of the client
            AGE (int): Client's age at the time of application
            YEARS_EMPLOYED (int): Number of years before the application
                the person started current employment
            FLAG_PHONE(str): Whether the phone provided is reachable
            CNT_FAM_MEMBERS (int): Number of family members does client have
            EMPLOYED (str): Whether the applicant is employed

        Returns:
            None

        """
        try:
            session = self.session
            applicant = Application(CODE_GENDER=CODE_GENDER,
                FLAG_OWN_CAR=FLAG_OWN_CAR,
                FLAG_OWN_REALTY=FLAG_OWN_REALTY,
                CNT_CHILDREN=CNT_CHILDREN,
                AMT_INCOME_TOTAL=AMT_INCOME_TOTAL,
                NAME_INCOME_TYPE=NAME_INCOME_TYPE,
                NAME_EDUCATION_TYPE=NAME_EDUCATION_TYPE,
                NAME_FAMILY_STATUS=NAME_FAMILY_STATUS,
                NAME_HOUSING_TYPE=NAME_HOUSING_TYPE,
                AGE=AGE,
                YEARS_EMPLOYED=YEARS_EMPLOYED,
                FLAG_MOBIL=FLAG_MOBIL,
                FLAG_WORK_PHONE=FLAG_WORK_PHONE,
                FLAG_PHONE=FLAG_PHONE,
                FLAG_EMAIL=FLAG_EMAIL,
                OCCUPATION_TYPE=OCCUPATION_TYPE,
                CNT_FAM_MEMBERS=CNT_FAM_MEMBERS,
                EMPLOYED=EMPLOYED)
            session.add(applicant)
            session.commit()
            logger.info("A new customer added to the database")
        except sqlalchemy.exc.OperationalError:
            logger.error('Failed to connect to server. '
                         'Please check if you are connected to Northwestern VPN')
    
    def add_application_df(self, input_path: str) -> None:
        """
        Add all the data in a csv file into the database
        Args:
            input_path: the path of the csv file
        Returns: None
        """

        session = self.session
        # Make the dataframe to a list of dictionaries to pass the data into the Pokemon class easily
        data_list = pd.read_csv(input_path).to_dict(orient='records')

        persist_list = []
        for data in data_list:
            persist_list.append(Application(**data))

        try:
            session.add_all(persist_list)
            session.commit()
        except sqlalchemy.exc.OperationalError:
            my_message = ('You might have connection error. Have you configured \n'
                          'SQLALCHEMY_DATABASE_URI variable correctly and connect to Northwestern VPN?')
            logger.error(f"{my_message} \n The original error message is: ", exc_info=True)
        except sqlalchemy.exc.IntegrityError:
            my_message = ('Have you already inserted the same record into the database before? \n'
                          'This database does not allow duplicate in the input-recommendation pair')
            logger.error(f"{my_message} \n The original error message is: ", exc_info=True)
        else:
            logger.info(f'{len(persist_list)} records were added to the table')
