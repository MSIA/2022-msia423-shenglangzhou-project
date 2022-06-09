'''
This file defines command-line arguments from the user and
delegates tasks to the appropriate module in src/.
'''
import argparse
import logging.config
import os
from webbrowser import get
import pkg_resources

import yaml
import joblib
import pandas as pd


from src.add_application import ApplicationManager, create_db
from src.s3 import upload_file_to_s3, download_file_from_s3
from src.acquire import import_application_data, clean, import_credit_data, clean_target, get_full_df
from src.features import featurize, get_ohe_data, get_user_df
from src.model import train_model
from src.score_model import compute_score
from src.evaluate import load_pred, load_test, compute_metrics
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logging.config.fileConfig(pkg_resources.resource_filename(__name__, 'config/logging/local.conf'),
                          disable_existing_loggers=False)
logger = logging.getLogger('loan-application-pipeline')

if __name__ == '__main__':

    # Add parsers for both creating a database and adding applications to it
    parser = argparse.ArgumentParser(description='Create and/or add data to database')
    parser.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser('create_db', description='Create database')
    sb_create.add_argument('--engine_string', default=SQLALCHEMY_DATABASE_URI,
                           help='SQLAlchemy connection URI for database')

    # Sub-parser for uploading data to s3
    sb_upload = subparsers.add_parser('upload_file_to_s3', help='Upload raw data to s3')
    sb_upload.add_argument('--s3_path1',
                           default='s3://2022-msia423-shenglang-zhou/raw/application_record.csv',
                           help='S3 data path to the data')
    sb_upload.add_argument('--local_path1', default='data/sample/application_record.csv',
                           help='local path to the data')
    sb_upload.add_argument('--s3_path2',
                           default='s3://2022-msia423-shenglang-zhou/raw/credit_record.csv',
                           help='S3 data path to the data')
    sb_upload.add_argument('--local_path2', default='data/sample/credit_record.csv',
                           help='local path to the data')

    # Sub-parser for downloading data from s3
    sb_download = subparsers.add_parser('download_file_from_s3', help='Download raw data from s3')
    sb_download.add_argument('--s3_path1',
                           default='s3://2022-msia423-shenglang-zhou/raw/application_record.csv',
                           help='S3 data path to the data')
    sb_download.add_argument('--local_path1', 
                            default='data/sample/application_record.csv',
                            help='local path to the data')
    sb_download.add_argument('--s3_path2',
                           default='s3://2022-msia423-shenglang-zhou/raw/credit_record.csv',
                           help='S3 data path to the data')
    sb_download.add_argument('--local_path2', default='data/sample/credit_record.csv',
                           help='local path to the data')

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser('ingest', description='Add cleaned data to database')
    sb_ingest.add_argument('--engine_string', default=os.environ.get('SQLALCHEMY_DATABASE_URI'),
                           help='SQLAlchemy Connection URI for database')
    sb_ingest.add_argument('--input', '-i', default='data/artifacts/ingest_data.csv',
                             help='Path to input data (optional, default = None)')

    # Sub-parser for acquiring, cleaning, and running model pipeline
    sb_pipeline = subparsers.add_parser('run_model_pipeline',
                                        description='Acquire data, clean data, '
                                                    'featurize data, and run model-pipeline')
    sb_pipeline.add_argument('--step', help='Which step to run',
                             choices=['clean', 'featurize', 'model','score', 'evaluate'])
    sb_pipeline.add_argument('--input', '-i', default=None,
                             help='Path to input data (optional, default = None)')
    sb_pipeline.add_argument('--config', default='config/config.yaml',
                             help='Path to configuration file')
    sb_pipeline.add_argument('--output', '-o', default=None,
                             help='Path to save output (optional, default = None)')
    sb_pipeline.add_argument('--output2', '-o2', default='data/artifacts/ingest_data.csv',
                             help='Path to save output (optional, default = None)')
    sb_pipeline.add_argument("--output_train", "-train", default="data/sample/train.csv", help="output file for train")
    sb_pipeline.add_argument("--output_test", "-test", default="data/sample/test.csv", help="output file for test")
    sb_pipeline.add_argument("--test", "-t", default= "data/sample/test.csv", help="path to the test file")
    sb_pipeline.add_argument("--model", "-m", default="models/randomforest.joblib", help="path to the model")
    sb_pipeline.add_argument("--prediction", "-p", default= "data/artifacts/evaluation_result.csv", help="path to the prediction file")
    args = parser.parse_args()
    sp_used = args.subparser_name

    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        am = ApplicationManager(engine_string=args.engine_string)
        am.add_application_df(args.input)
        am.close()
    elif sp_used == 'upload_file_to_s3':
        upload_file_to_s3(args.local_path1, args.s3_path1)
        upload_file_to_s3(args.local_path2, args.s3_path2)
    elif sp_used == 'download_file_from_s3':
        download_file_from_s3(args.local_path1, args.s3_path1)
        download_file_from_s3(args.local_path2, args.s3_path2)
    elif sp_used == 'run_model_pipeline':
        # load yaml configuration file
        try:
            with open(args.config, 'r') as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
                logger.info('Configuration file loaded from %s' % args.config)
        except FileNotFoundError:
            logger.error('Configuration file from %s is not found' % args.config)

        if args.input is not None:
            input = pd.read_csv(args.input)
            logger.info('Input data loaded from %s', args.input)

        if args.step == 'clean':
            # import raw data and clean data
            raw1 = import_application_data(**conf['acquire']['import_application_data'])
            raw2= import_credit_data(**conf['acquire']['import_credit_data'])
            df_app = clean(raw1, **conf['acquire']['clean'])
            df_credit=clean_target(raw2,**conf['acquire']['clean_target'])
            output=get_full_df(df_app,df_credit,**conf['acquire']['get_full_df'])
        elif args.step == 'featurize':
            # generate new features from cleaned data and one-hot encode
            featurized = featurize(input, **conf['features']['featurize'])
            output = get_ohe_data(featurized, **conf['features']['get_ohe_data'])
            output2= get_user_df(featurized, **conf['features']['get_user_df'])
            if args.output2 is not None:
                # save the data that needs to be ingested
                output2.to_csv(args.output2, index=False)
                logger.info('Output saved to %s', args.output2)
        elif args.step == 'model':
            # train model & evaluate results
            output, y_test, y_train,X_test,X_train = train_model(input, **conf['model']['train_model'])
            
            train = pd.concat([X_train, y_train], axis=1)
            test = pd.concat([X_test, y_test], axis=1)
            train.to_csv(args.output_train, index=False)
            test.to_csv(args.output_test, index=False)
            
        elif args.step == 'score':
            test = pd.read_csv(args.test)
            loaded_rf = joblib.load(args.model)
            # evaluate the model result
            output=compute_score(loaded_rf, test, **conf['score_model']['compute_score'])

        elif args.step == 'evaluate':
            
            
       
            param_py = conf['evaluate']

            # do the prediction and save to file
            test = pd.read_csv(args.test)
            prediction = pd.read_csv(args.prediction)

            y_test = load_test(args.test, **param_py["load_test"])
            proba, binary = load_pred(args.prediction, **param_py["load_pred"])

            result = compute_metrics(y_test, proba, binary, **param_py["compute_metrics"])
        
            with open(args.output, "w") as file:
                if "auc" in result:
                    file.write('AUC on test: %0.3f \n\n' % result["auc"])
                if "accuracy" in result:
                    file.write('Accuracy on test: %0.3f\n\n' % result["accuracy"])
                if "confusion" in result:
                    file.write('Confusion matrix:\n')
                    file.write(pd.DataFrame(result["confusion"],
                            index=['Actual negative','Actual positive'],
                            columns=['Predicted negative', 'Predicted positive']).to_string())
                    file.write('\n\n')
                if "classification_report" in result:
                    file.write('classification_report:\n')
                    file.write(result["classification_report"])

       

    

        if args.output is not None:
            if args.step != 'model' and args.step != 'evaluate':
                # save intermediate artifacts in the model pipeline
                output.to_csv(args.output, index=False)
                logger.info('Output saved to %s', args.output)
            elif args.step == 'model':
                # save the trained model
                joblib.dump(output, args.output)
                logger.info('Trained model object saved to %s', args.output)
        

    else:
        parser.print_help()
