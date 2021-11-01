from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

app.config['UPLOADED_FILES_DEST'] = os.getcwd()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from routes.users import routes
from routes.authenticate import routes
from routes.surveys import routes
import models
import logging
import http.client


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Saigon'

USE_I18N = True

USE_L10N = True

USE_TZ = True


logging.basicConfig(level=logging.DEBUG)
http.client.HTTPConnection.debuglevel=5