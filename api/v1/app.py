#!/usr/bin/python3
"""
API
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
import os

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

app = Flask(__name__)
"""<----------------- view routes ----------------->"""
app.register_blueprint(app_views)


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
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
