#!/usr/bin/python3
"""
API
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
"""<----------------- view routes ----------------->"""
app.register_blueprint(app_views)
CORS(app, origins='0.0.0.0')


@app.teardown_appcontext
def teardown_db(exception=None):
    """ This function called each time the database is updated
    """
    storage.close()


"""<---------------- error handling --------------->"""
@app.errorhandler(400)
def name_not_found(msg):
    """ This function handels status_code '400'
    """
    return jsonify({'error': msg.description}), 400


@app.errorhandler(404)
def not_found(error):
    """ This function handels status_code '404'
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
