from flask import Blueprint
from flask_restx import Api, Resource, fields
from werkzeug.datastructures import FileStorage
import pandas as pd
from flask import request
from sqlalchemy import MetaData, Column, Integer, Float, String, Table, text
from sqlalchemy.dialects.mysql import TINYINT


import os
from datetime import datetime, timezone

from app.db_models.table_classes import Credentials, UserDataset
from app.extensions import db


dataset_api_blueprint = Blueprint('dataset_api', __name__)
api = Api(dataset_api_blueprint, doc='/')

### Business Pipeline 
dataset_namespace = api.namespace('', description='Dataset API')


user_model = api.model('user_model', {
    'email': fields.String(required=True, description="The user's email")
})

user_dataset_model = api.model('user_dataset_model', {
    'tablename': fields.String(required=True, description="The selected user table name")
})

upload_parser = api.parser()
upload_parser.add_argument('email', type=str, required=True)
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)
@dataset_namespace.route('')
class UserDatasetResource(Resource):
    @dataset_namespace.expect(upload_parser)
    def post(self):
        """Upload new file"""
        try:
            data = request.args
            email = data.get('email')
            uploaded_file = request.files['file']
            if uploaded_file.filename.endswith('.csv'):
                filename_split = os.path.splitext(uploaded_file.filename)
                filename = filename_split[0]
                if "." in filename:
                    filename = filename.replace(".", "_")

                # Check user exists
                query_user = Credentials.query.filter_by(email = email).first()
                if not query_user:
                    raise Exception('User not found')
                df = pd.read_csv(uploaded_file, delimiter=None)
                # df['is_anomaly'] = False
                tablename = f'{query_user.user_id}_{filename}'
                created_timestamp = datetime.now(timezone.utc)

                # check if the dataset has already been uploaded by the user
                has_dataset = UserDataset.query.filter_by(user_id_fk=query_user.user_id, filename=filename).first()
                if has_dataset:
                    return {'message': f'The table {tablename} already exists.'}, 200
                
                # insert the info in user dataset
                new_user_dataset = UserDataset(user_id_fk=query_user.user_id, filename=filename, stored_tablename=tablename, created_timestamp=created_timestamp)
                db.session.add(new_user_dataset)
                db.session.commit()

                # create new table for the dataset in database
                metadata = MetaData()
                columns = []
                columns.append(Column('id', Integer, primary_key=True, autoincrement=True))
                for col, data_type in self.infer_data_types(df).items():
                    if data_type == 'INT':
                        columns.append(Column(col, Integer))
                    elif data_type == 'FLOAT':
                        columns.append(Column(col, Float))
                    elif data_type == 'TINYINT':
                        columns.append(Column(col, TINYINT))
                    else:
                        columns.append(Column(col, String(255)))  # Set length to 255 for VARCHAR columns
                table = Table(
                    tablename,
                    metadata,
                    *columns
                )
                metadata.create_all(db.engine)
                df.to_sql(tablename, con=db.engine, if_exists='append', index=False)
                return {'message': f'Table {filename} created and data inserted successfully.'}, 201
            else:
                return {'message': 'file uploaded is not csv'}, 400

        except Exception as e:
            return {'error': str(e)}, 500



    @staticmethod
    def infer_data_types(df):
        data_types = {}
        for column in df.columns:
            dtype = str(df[column].dtype)
            if 'int' in dtype:
                data_types[column] = 'INT'
            elif 'float' in dtype:
                data_types[column] = 'FLOAT'
            elif 'bool' in dtype:
                data_types[column] = 'TINYINT'
            else:
                data_types[column] = 'VARCHAR(255)'
        return data_types

@dataset_namespace.route('/list_user_datasets')
class GetUserDatasetTables(Resource):
    @dataset_namespace.expect(user_model)
    def post(self):
        """Present all tables in user's database"""
        try:
            data = request.get_json()
            email = data.get('email')

            # Check user exists
            query_user = Credentials.query.filter_by(email = email).first()
            if not query_user:
                return {'error': 'User not found'}, 404

            # Get user's datasets
            user_datasets = UserDataset.query.filter_by(user_id_fk=query_user.user_id).all()
            user_tables = []
            for user_dataset in user_datasets:
                user_tables.append(user_dataset.stored_tablename)
            return {'tables': user_tables}, 200
        except Exception as e:
            return {'error': f'Error: {e}'}, 500
        
@dataset_namespace.route('/get_user_dataset_data')
class GetUserDataset(Resource):
    @dataset_namespace.expect(user_dataset_model)
    def post(self):
        try:
            data = request.get_json()
            tablename = data.get('tablename')

            # check if the table exists
            selected_table = UserDataset.query.filter_by(stored_tablename=tablename).first()
            if not selected_table:
                return {'error': 'table not found'}, 404
            
            select_query = text("SELECT * FROM " + tablename)
            with db.engine.begin() as conn:
                result = pd.read_sql_query(select_query, conn)
                dataset_dict = result.to_dict(orient='records')
                return {'message': 'list all data in dataset', 'dataset': dataset_dict}, 200

        except Exception as e:
            return {'error': f'Error: {e}'}, 500
