from flask import Blueprint
from flask_restx import Api, Resource, fields
import pandas as pd
from flask import request
from datetime import datetime, timezone
from sqlalchemy import text
from sklearn.metrics import accuracy_score, confusion_matrix

from app.db_models.table_classes import MLDLModel, UserDataset, AnomalyLog, Anomaly, Credentials
from app.extensions import db
from app.extensions import mlflow
from app.mldl_classes import ChinIsolationForestCls
import json

anamolies_api_blueprint = Blueprint('anomalies_api', __name__)
api = Api(anamolies_api_blueprint, doc='/')

### ML DL Model
anamolies_namespace = api.namespace('', description='Test Model for Anomalies')

ML_Test_Data= api.model('ML_Test_Data', {
    'email': fields.String(required=True, description='user email'),
    'model_name': fields.String(required=True, description='ML DL model name'),
    'model_version': fields.Integer(required=True, description='ML DL model version'),
    'stored_tablename': fields.String(required=True, description='dataset name')
})

Anomalies_Data = api.model('Anomalies_Data', {
    'anomaly_log_id': fields.Integer(required=True, description='Anomaly Log ID')
})


@anamolies_namespace.route('/test_model_with_dataset')
class TestModel(Resource):
    @anamolies_namespace.expect(ML_Test_Data)
    def post(self):
        try :

            data = request.get_json()
            model_name = data.get('model_name')
            model_version = data.get('model_version')
            email = data.get('email')
            stored_tablename = data.get('stored_tablename')

            usr = Credentials.query.filter_by(email = email).first()
            if not usr:
                return {"error": "Not user found"}, 400 
            
            mldlmodel_result = MLDLModel.query.filter_by(model_name=model_name, model_version=model_version).first()
            if not mldlmodel_result:
                return {"error": "Model does not exist in database"}, 400

            # model uri for the above model
            model_uri = "models:/{}/{}".format(model_name, model_version)
            
            # Load the model and access the custom metadata
            loaded_model = mlflow.pyfunc.load_model(model_uri=model_uri)
            if not loaded_model:
                return {"error": "Model does not exist in MLFLOW"}, 400

            has_dataset = UserDataset.query.filter_by(stored_tablename=stored_tablename).first()
            if not has_dataset:
                return {'error': 'table not found'}, 404
            isolation_forest_cls = ChinIsolationForestCls(None)
            select_query = text("SELECT * FROM " + stored_tablename)
            ids = []
            test_data = None
            with db.engine.begin() as conn:
                result = pd.read_sql_query(select_query, conn)
                ids = result['id'].values
                result.drop('id', axis=1, inplace=True)
                isolation_forest_cls.cc_trans_df = result
                isolation_forest_cls.perform_pipeline()
                _, _, X_test, y_test, ml_metadata = isolation_forest_cls.ml_train_pipeline(is_train=False)
            predictions = loaded_model.predict(X_test)

            # Isolation forest needs to deal with non 1


            # Find indices of the specific value
            indices = []
            indices = [ids[index] for index, element in enumerate(predictions) if element == 1]

            indices_dict = {}

            # Store indices in the dictionary if the value is found
            if indices:
                indices_dict[1] = indices

            # predictions = predictions == 1
            # accuracy = accuracy_score(y_test, predictions)
            # conf_matrix = confusion_matrix(y_test, predictions)
            # print(f'accuracy: {accuracy}  conf_matrix: {conf_matrix} indices: {indices_dict}')
            
            anomaly_log1 = AnomalyLog(user_dataset_id_fk=usr.user_id, model_id_fk=mldlmodel_result.model_id, created_timestamp= datetime.now(timezone.utc))
            db.session.add(anomaly_log1)
            db.session.commit()
            for id in indices:
                anomaly_instance = Anomaly(anomaly_log_id_fk=anomaly_log1.anomaly_log_id, anomaly_instances_ids=id)
                db.session.add(anomaly_instance)
            db.session.commit()

            return {'message': 'all workflow completes'}, 200
        
        except Exception as e:
            return {'error': str(e)}, 500

@anamolies_namespace.route('/get_anomalies')
class TestModel(Resource):
    @anamolies_namespace.expect(Anomalies_Data)
    def post(self):
        try :
            data = request.get_json()
            anomaly_log_id = data.get('anomaly_log_id')
            anomaly_log_res = AnomalyLog.query.filter_by(anomaly_log_id=anomaly_log_id).first()
            if not anomaly_log_res:
                return {'error': 'no anomaly log found'}, 404
            anomalies_res = Anomaly.query.filter_by(anomaly_log_id_fk=anomaly_log_res.anomaly_log_id).all()
            anomaly_ids =[]
            for anomaly_data in anomalies_res:
                anomaly_ids.append(anomaly_data.anomaly_instances_ids)
            return {'message': 'all workflow completes', 'anomalies': anomaly_ids}, 200
        
        except Exception as e:
            return {'error': str(e)}, 500