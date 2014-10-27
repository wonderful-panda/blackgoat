# coding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

def setup(basedir, config=None, template_folder=None, static_folder=None):
    import os
    from urllib import pathname2url
    database_uri = \
            'sqlite:' + pathname2url(os.path.join(basedir, 'blackgoat.db'))
    global app
    global db
    app = Flask(__name__,
                template_folder=template_folder or 'templates',
                static_folder=static_folder or 'static')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    if config:
        app.config.update(config)
    db = SQLAlchemy(app)
    import blackgoat.views
    assert blackgoat.views # to avoid pep8 warning 'Imported but unused'

    return app, db

