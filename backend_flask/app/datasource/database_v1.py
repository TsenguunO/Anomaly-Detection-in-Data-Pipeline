import os
import mysql.connector as msql
from mysql.connector import Error
import pandas as pd
from flask import Flask, request
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage


app = Flask(__name__)
api = Api(app, version='1.0', title='Database')

# Replace these variables with your database connection details
db_user = 'root'
db_password = 'mysql123' # change to your mysql password


class Database(Resource):
    @api.doc('upload_file')
    @api.expect(api.parser().add_argument('file', location='files', type=FileStorage, required=True))
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Upload new file"""
        try:
            # Get the uploaded file
            uploaded_file = request.files['file']
            if uploaded_file.filename.endswith('.csv'):
                file_name = os.path.splitext(uploaded_file.filename)[0]
                if "." in file_name:
                    file_name = file_name.replace(".", "")
                df = pd.read_csv(uploaded_file, delimiter=None)
                column_data_types = self.infer_data_types(df)
                # Get the column names from the first row of the csv file
                column_names = list(df.columns)
                # Create a comma-separated string of column names
                column_string = ",".join(column_names)
                # Create a comma-separated string of placeholders for the column values
                placeholder_string = ",".join(["%s"] * len(column_names))
                user_id = request.environ['SERVER_PORT']
                # Connect to MySQL
                conn = msql.connect(user=db_user, password=db_password)

                if conn.is_connected():
                    cursor = conn.cursor()
                    # Create the database if it does not exist
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS user_{user_id}")
                    conn.database = f"user_{user_id}"  # Switch to the database

                    cursor.execute(f"SHOW TABLES LIKE '{file_name}'")
                    existing_table = cursor.fetchone()
                    if existing_table:
                        # Table already exists, return a message indicating it's already there
                        return {'user_id': user_id,
                                'message': f'The table "{file_name}" already exists in the database.'}, 200
                    # Create a table for the csv file if it does not exist
                    create_table_query = f"CREATE TABLE IF NOT EXISTS {file_name} ("
                    for column, data_type in column_data_types.items():
                        create_table_query += f"{column} {data_type}, "
                    create_table_query = create_table_query.rstrip(", ") + ")"
                    cursor.execute(create_table_query)
                    # Insert the csv data into the table
                    for row in df.itertuples(index=False):
                        insert_query = f'INSERT INTO {file_name} ({column_string}) VALUES ({placeholder_string})'
                        cursor.execute(insert_query, row)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return {'user_id': user_id, 'message': 'File uploaded and saved to the database successfully.'}, 201
                else:
                    return {'error': 'Database connection failed.'}, 500
            else:
                return {'error': 'Please upload a csv file.'}, 400
        except Error as e:
            return {'error': f'Error while connecting to MySQL: {e}'}, 500

    @api.doc('get_tables')
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self):
        """Present all tables in user's database"""
        try:
            user_id = request.environ['SERVER_PORT']
            tables = self.get_user_tables(user_id)
            return {'user_id': user_id, 'tables': tables}, 200
        except Error as e:
            return {'error': f'Error: {e}'}, 500

    @staticmethod
    # to get data type in uploaded data
    def infer_data_types(df):
        data_types = {}
        for column in df.columns:
            dtype = str(df[column].dtype)
            if 'int' in dtype:
                data_types[column] = 'INT'
            elif 'float' in dtype:
                data_types[column] = 'FLOAT'
            else:
                data_types[column] = 'VARCHAR(255)'
        return data_types

    @staticmethod
    def get_user_tables(user_id):
        try:
            conn = msql.connect(user=db_user, password=db_password, database=f'user_{user_id}')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                cursor.close()
                conn.close()
                return [table[0] for table in tables]
            else:
                return []
        except Error as e:
            return []


api.add_resource(Database, '/database')


class Preview(Resource):
    @api.doc('preview_table')
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self, table_name):
        """show first 5 rows of selected table"""
        try:
            user_id = request.environ['SERVER_PORT']
            conn = msql.connect(user=db_user, password=db_password, database=f'user_{user_id}')
            if conn.is_connected():
                query = f"SELECT * FROM {table_name} LIMIT 5"
                df = pd.read_sql(query, conn)
                conn.close()
                return df.to_json(orient='records'), 200
            else:
                return {'error': 'Database connection failed.'}, 500
        except Error as e:
            return {'error': f'Error: {e}'}, 500


api.add_resource(Preview, '/preview/<string:table_name>')

if __name__ == '__main__':
    app.run(debug=True,port=5000) # change port number to test different user scenario 5000, 5001, 5002 etc

