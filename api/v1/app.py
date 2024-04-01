#!/usr/bin/python3
"""app.py to connect to API Flask"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(exception):
    return (jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage upon teardown"""
    storage.close()


# Add a blank line here
if __name__ == "__main__":
    if getenv('HBNB_API_HOST') and getenv('HBNB_API_PORT'):
        app.run(host=getenv('HBNB_API_HOST'), port=getenv('HBNB_API_PORT'),
                threaded=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True)
