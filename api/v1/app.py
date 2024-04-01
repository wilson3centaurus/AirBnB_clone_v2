#!/usr/bin/python3
"""app.py module
"""
from flask import Flask, Blueprint, jsonify
from werkzeug.exceptions import HTTPException
import os
app = Flask(__name__)
from models import storage
from api.v1.views import app_views


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """teardown method to close storage
    """
    storage.close()
    

@app.errorhandler(HTTPException)
def handle_exception(e):
    """handle_exception method
    """
    response = {
        "error": e.name,
    }
    return jsonify(response), e.code


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    app.run(port=port, host=host, threaded=True, debug=True)
