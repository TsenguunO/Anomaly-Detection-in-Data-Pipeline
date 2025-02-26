import sys
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy_utils import database_exists, create_database, drop_database

engine_url = "mysql+pymysql://root:gptea_admin@localhost:3306/gpteadb"
engine_url_mlflow = "mysql+pymysql://root:gptea_admin@localhost:3306/mlflowdb"
engine = create_engine(engine_url)
engine_mlflow = create_engine(engine_url_mlflow)

opt = sys.argv[:]
if len(opt) == 2 or len(opt) == 3:
    print(opt[1])
    if opt[1] == '-r':
        if database_exists(engine.url):
            drop_database(engine_url)
            print("Backend databse is now removed.")
        if database_exists(engine_mlflow.url):
            drop_database(engine_url_mlflow)
            print("mlflow databse is now removed.")

if not database_exists(engine.url):
    print("creating database ...... ")
    create_database(engine_url)
    create_database(engine_url_mlflow)
    if database_exists(engine.url):
        print("backend database created.")
    if database_exists(engine_mlflow.url):
        print("mlflow database created.")

    if len(opt) == 3:
        if opt[2] == '-o':
            metadata = MetaData()

            credentials = Table('credentials', metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('email', String(255), unique=True, nullable=False), 
                Column('password', String(255), nullable=False),
                Column('created_timestamp', DateTime, nullable=False, default=datetime.utcnow)
            )

            user_log = Table('user_log', metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('email', String(255), unique=False, nullable=False), 
                Column('log_timestamp', DateTime, nullable=False, default=datetime.utcnow)
            )

            pipeline = Table('pipeline', metadata,
                Column('pipeline_id', Integer, primary_key=True, autoincrement=True),
                Column('pipeline_name', String(255), unique=True, nullable=False), 
                Column('email', String(255), nullable=False), 
                Column('created_timestamp', DateTime, nullable=False, default=datetime.utcnow)
            )
            model = Table('model', metadata,
                Column('model_id', Integer, primary_key=True, autoincrement=True),
                Column('model_name', String(255), unique=True, nullable=False), 
                Column('created_timestamp', DateTime, nullable=False, default=datetime.utcnow)
            )

            pipeline_model = Table('pipeline_model', metadata,
                Column('pipeline_model_id', Integer, primary_key=True, autoincrement=True),
                Column('pipeline_name', String(255), ForeignKey('pipeline.pipeline_name'), nullable=False),
                Column('model_name', String(255), ForeignKey('model.model_name'), nullable=False),
                Column('created_timestamp', DateTime, nullable=False, default=datetime.utcnow)
            )
            anomaly_log = Table('anomaly_log', metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('dataset', String(255), nullable=False),
                Column('pipeline_name', String(255), ForeignKey('pipeline.pipeline_name'), nullable=False),
                Column('model_name', String(255), ForeignKey('model.model_name'), nullable=False),
                Column('email', String(255)),
                Column('timestamp', DateTime),
                Column('anomaly_type', String(255)),
                Column('number_of_instances', Integer),
                Column('user_action', String(255)),
                Column('created_timestamp', DateTime, default=datetime.utcnow)
            )
            metadata.create_all(engine, checkfirst=True)