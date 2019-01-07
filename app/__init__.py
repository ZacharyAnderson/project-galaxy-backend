""" This module initiliazes the Flask application and Database  """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models, datastore
