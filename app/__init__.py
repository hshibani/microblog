# package - flask
# class - Flask
from flask import Flask
# config - package
# Config - class
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os



# Creating an instance of the application, naming it app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # db instance representing the db object
migrate = Migrate(app, db) # migrate instance representing the migration engine
login = LoginManager(app)
# set the view function that handles login(routes.py login() or the url_for name)
# this is for landing in the right page after authentication
# after attempting to access a protected page(one with login_required decorator set) without login
login.login_view = 'login'

# logging using Python's logging package
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


# app here is the package name, routes is the class or a module, models is a module representing
# the structure of the db
from app import routes, models, errors