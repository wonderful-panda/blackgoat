# coding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
if hasattr(sys, 'frozen'):
    from jinja2 import PackageLoader
    app.jinja_loader = PackageLoader(__name__, 'templates')
db = SQLAlchemy(app)
import blackgoat.views

def setup_app(database_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri



