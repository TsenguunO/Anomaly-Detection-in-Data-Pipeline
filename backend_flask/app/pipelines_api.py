from flask import Blueprint
from flask_restx import Api, Resource, fields
import pandas as pd
from flask import request
from sqlalchemy import text
from datetime import datetime, timezone

from app.db_models.table_classes import Pipeline
from app.extensions import db


pipelines_api_blueprint = Blueprint('pipelines_api', __name__)
api = Api(pipelines_api_blueprint, doc='/')

### Business Pipeline 
pipeline_namespace = api.namespace('', description='Business Pipelines')
Pipeline_model= api.model('Pipeline', {
    'pipeline_name': fields.String(required=True, description='business pipeline name')
})

@pipeline_namespace.route('')
class PipelineResource(Resource):
    @pipeline_namespace.expect(Pipeline_model)
    def post(self):
        data = request.get_json()
        pipeline_name = data.get('pipeline_name')
        # email = data.get('email')
        created_timestamp = datetime.now(timezone.utc)

        if not pipeline_name:
            return {"error": "pipeline is required"}, 400
        
        pipeline_query_result = Pipeline.query.filter_by(pipeline_name = pipeline_name).first()
        if pipeline_query_result:
            return {"error": "Pipeline already exists"}, 400

        else:
            new_biz_pipeline = Pipeline(pipeline_name = pipeline_name, created_timestamp = created_timestamp)
            db.session.add(new_biz_pipeline)
            db.session.commit()
            return {'message': 'Business Pipeline added successfully'}, 201

@pipeline_namespace.route('/get_all_pipelines')
class GetPipelines(Resource):
    def get(self):
        select_query = text("SELECT * FROM pipeline")

        with db.engine.begin() as conn:
            result = pd.read_sql_query(select_query, conn)
            if result.empty:
                return {"error": "No pipeline association found"}, 400
            result['created_timestamp'] = result['created_timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            pipeline_list = result.to_dict(orient='records')
            return {'message': 'Listed all pipelines', 'pipeline_list': pipeline_list}, 200
        
### Nice to have  - Delete template

