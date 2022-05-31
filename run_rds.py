"""Creates two tables to contain application records and credit records"""
import os
import logging
import sqlalchemy as sql
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

engine_string = os.getenv("SQLALCHEMY_DATABASE_URI")
if engine_string is None:
    raise RuntimeError("SQLALCHEMY_DATABASE_URI environment variable not set; exiting")
# engine_string = "mysql+pymysql://dylan:Zz990915@nu-msia423-shenglang.c32qnaesjuwf.us-east-1.rds.amazonaws.com:3306/msia_db"

# set up looging config
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__file__)

Base = declarative_base()


class Application(Base):
    """Creates a data model for the database to be set up for capturing past applications."""

    __tablename__ = "application_details"

    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    CODE_GENDER  = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    FLAG_OWN_CAR = sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=False)
    FLAG_OWN_REALTY= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    CNT_CHILDREN= sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    AMT_INCOME_TOTAL= sqlalchemy.Column(sqlalchemy.Float, unique=False, nullable=True)
    NAME_INCOME_TYPE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    NAME_EDUCATION_TYPE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    NAME_FAMILY_STATUS= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    NAME_HOUSING_TYPE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True)
    DAYS_BIRTH= sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    DAYS_EMPLOYED= sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)
    FLAG_MOBIL= sqlalchemy.Column(sqlalchemy.Boolean, unique=False, nullable=True)
    FLAG_WORK_PHONE= sqlalchemy.Column(sqlalchemy.Boolean, unique=False, nullable=True)
    FLAG_PHONE= sqlalchemy.Column(sqlalchemy.Boolean, unique=False, nullable=True)
    FLAG_EMAIL= sqlalchemy.Column(sqlalchemy.Boolean, unique=False, nullable=True)
    OCCUPATION_TYPE= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True) 
    CNT_FAM_MEMBERS= sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True) 

   

class Credit(Base):
    """Creates a data model for the database to be set up for capturing past applicants credit record."""
    __tablename__ = 'credit_record'
    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    MONTHS_BALANCE= sqlalchemy.Column(sqlalchemy.String(100), primary_key=True) 
    STATUS= sqlalchemy.Column(sqlalchemy.String(100), unique=False, nullable=True) 

class New_applications(Base):
    """Creates a data model for the database to be set up for capturing new applications."""
    __tablename__ = 'new_application'
    

  

if __name__ == "__main__":
    # set up mysql connection
    engine = sql.create_engine(engine_string)

    # test database connection
    try:
        engine.connect()
    except sqlalchemy.exc.OperationalError as e:
        logger.error("Could not connect to database!")
        logger.debug("Database URI: %s", )
        raise e

    # create the tracks table
    Base.metadata.create_all(engine)

    # create a db session
    Session = sessionmaker(bind=engine)
    session = Session()

   
    session.commit()

    


    session.close()
