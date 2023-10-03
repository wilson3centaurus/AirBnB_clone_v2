#!/usr/bin/python3

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    This function is a Flask decorator that is used to register a function
    to be called when the application context is torn down.
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Handles the 404 error in a Flask application.

    :param exception: The exception object that represents the 404 error.
    :return: A JSON response with the error message "Not found" and a status code of 404.
    """
    data = {"error": "Not found"}
    return jsonify(data), 404


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
