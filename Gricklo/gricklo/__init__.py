from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from os.path import join, dirname, realpath, os


UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] ='12345'
from flask_migrate import Migrate
migrate = Migrate(app, db)

from gricklo.controlers import *