#!/usr/bin/python3
""" creating an app file for defining end points """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)


app.register_blueprint(app_views)

if __name__ == '__main__':
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
