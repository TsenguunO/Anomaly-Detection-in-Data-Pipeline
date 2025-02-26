# app.py

from flask import Flask, render_template
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from app.user_api import user_api_blueprint as user_bp
from app.mldl_api import mldl_api_blueprint as mldl_bp
from app.pipelines_api import pipelines_api_blueprint as pipeline_bp
from app.dataset_api import dataset_api_blueprint as dataset_bp
from app.anomalies_api import anamolies_api_blueprint as anamolies_bp
from app.extensions import db
from app.db_models.table_classes import create_samples

from sqlalchemy import inspect

from app.db_models.table_classes import QuestionName

app = Flask(__name__)
app.config.from_pyfile("config.py")
CORS(app)

bp_dict = {'user_bp': '/api/',
           'mldl_bp': '/api/model/',
           'pipeline_bp': '/api/pipeline/',
           'dataset_bp': '/api/dataset/',
           'anomalies_bp' : '/api/anomalies'}

app.register_blueprint(user_bp, url_prefix=bp_dict['user_bp'])
app.register_blueprint(mldl_bp, url_prefix=bp_dict['mldl_bp'])
app.register_blueprint(pipeline_bp, url_prefix=bp_dict['pipeline_bp'])
app.register_blueprint(dataset_bp, url_prefix=bp_dict['dataset_bp'])
app.register_blueprint(anamolies_bp, url_prefix=bp_dict['anomalies_bp'])

    
@app.route('/')
def index_page():
    return render_template('index.html', utc_dt = datetime.now(timezone.utc), bp_dict = bp_dict)


if __name__ == "__main__":
    # init the db extension
    db.init_app(app)

    with app.app_context():
        # Create an inspector object
        inspector = inspect(db.engine)

        # Check if a table exists
        table_name = 'credentials'
        table_exists = inspector.has_table(table_name)

        if not table_exists:
            db.create_all()
            create_samples()

    app.run(host="0.0.0.0", port=8000, debug=True)
