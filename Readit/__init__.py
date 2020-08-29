# Readit/__init__.py

from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#from mysql.connector import mysqlconnector

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey7856gfdfr'
#############################################
########### DATABASE SETUP ##################
#############################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="vraj",
#     password="mySQL8989",
#     hostname="localhost",
#     databasename="data",
# )
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


db = SQLAlchemy(app)
Migrate(app, db)

#############################################
########### LOGIN CONFIGS ###################
#############################################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


#############################################

from Readit.blog_posts.views import blog_posts
from Readit.users.views import users
from Readit.error_pages.handlers import error_pages
from Readit.core.views import core


app.register_blueprint(core)

app.register_blueprint(error_pages)

app.register_blueprint(users)

app.register_blueprint(blog_posts)
