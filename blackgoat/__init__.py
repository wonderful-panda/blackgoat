# coding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from os.path import abspath, dirname

scriptdir = dirname(abspath(__file__)).replace('\\', '/')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///{0}/blackgoat.db'.format(scriptdir)
db = SQLAlchemy(app)

import blackgoat.views

