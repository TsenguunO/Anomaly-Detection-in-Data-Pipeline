from flask import Blueprint
from flask_restx import Api, Resource, fields
import pandas as pd
from flask import request
from datetime import datetime, timezone
from sqlalchemy import text

from app.db_models.table_classes import MLDLModel
from app.extensions import db

mldl_api_blueprint = Blueprint('mldl_api', __name__)
api = Api(mldl_api_blueprint, doc='/')

### ML DL Model
model_namespace = api.namespace('', description='ML DL models')
ML_model= api.model('ML_model', {
    'model_name': fields.String(required=True, description='ML DL model name'),
    'model_version': fields.Integer(required=True, description='ML DL model version')
})

ML_Test_Data= api.model('ML_Test_Data', {
    'model_name': fields.String(required=True, description='ML DL model name'),
    'model_version': fields.Integer(required=True, description='ML DL model version'),
    'dataset_name': fields.String(required=True, description='dataset name')
})

@model_namespace.route('')
class Model(Resource):
    @model_namespace.expect(ML_model)
    def post(self):
        data = request.get_json()
        model_name = data.get('model_name')
        model_version = data.get('model_version')
        created_timestamp = datetime.now(timezone.utc)
        
        if not model_name:
            return {"error": "model name is required"}, 400
        
        mldlmodel_result = MLDLModel.query.filter_by(model_name=model_name, model_version=model_version).first()
        if mldlmodel_result:
            return {"error": "Model already exists"}, 400
        else:
            new_mldl_model = MLDLModel(model_name = model_name, model_version = model_version, created_timestamp = created_timestamp)
            db.session.add(new_mldl_model)
            db.session.commit()
            return {'message': 'Model added successfully'}, 201

@model_namespace.route('/get_all_models')
class GetModels(Resource):
    def get(self):

        select_query = text("SELECT * FROM mldl_model")
        with db.engine.begin() as conn:
            result = pd.read_sql_query(select_query, conn)
            if result.empty:
                return {"error": "No model found"}, 400
            result['created_timestamp'] = result['created_timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            models_list = result.to_dict(orient='records')
            return {'message': 'Listed all models', 'model_list': models_list}, 200


   