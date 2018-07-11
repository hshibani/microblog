# package - flask
# class - Flask
from flask import Flask
# config - package
# Config - class
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


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

# app here is the package name, routes is the class or a module, models is a module representing
# the structure of the db
from app import routes, models