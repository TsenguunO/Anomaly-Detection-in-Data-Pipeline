import os

basedir = os.path.abspath(os.path.dirname(__file__))


# General Config
ENVIRONMENT = "development"
FLASK_APP = "'Anomaly Detection API'"
FLASK_DEBUG = True
# SECRET_KEY = "GDtfD^&$%@^8tgYjD"

##db setup
#change the password if you using different one
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:gptea_admin@localhost:3306/gpteadb'
SQLALCHEMY_TRACK_MODIFICATIONS = False

