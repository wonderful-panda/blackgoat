# coding: utf-8
import flask
from blackgoat import app
from blackgoat.models import Message

@app.route('/')
def index():
    messages = Message.query.order_by('id desc').limit(10).all()
    return flask.render_template('index.html', messages=messages)

@app.route('/message/<id>')
def message(id):
    msg = Message.query.get(id)
    return flask.render_template('message.html', msg=msg)

@app.route('/raw/<id>')
def raw(id):
    msg = Message.query.get(id)
    return flask.Response(msg.raw, mimetype='text/plain')

