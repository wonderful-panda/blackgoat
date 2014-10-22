# coding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from os.path import abspath, dirname
import sys

app = Flask(__name__)
if hasattr(sys, 'frozen'):
    basedir = dirname(abspath(sys.executable))
    from jinja2 import PackageLoader
    app.jinja_loader = PackageLoader(__name__, 'templates')
else:
    basedir = dirname(abspath(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///{0}/blackgoat.db'.format(basedir.replace('\\', '/'))
db = SQLAlchemy(app)

import blackgoat.views

