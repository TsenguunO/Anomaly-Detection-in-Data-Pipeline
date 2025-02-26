from flask_sqlalchemy import SQLAlchemy
import mlflow
db = SQLAlchemy()
mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

pretrained_model = {
    1 : {'model_name': 'Isolation Forest', 'version': 1},
    2 : {'model_name': 'Autoencoder', 'version': 1},
    3 : {'model_name': 'Random Forest', 'version': 1}
    }