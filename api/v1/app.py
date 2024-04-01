#!/usr/bin/python3
"""app.py to connect to API"""
from api.v1.views import app_views
from models import storage
from flask import Flask, Blueprint, jsonify, make_response
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    api_host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host=api_host, port=int(api_port), threaded=True)
    
