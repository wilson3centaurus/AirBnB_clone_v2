#!/usr/bin/python3
"""Flask application"""
from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """teardown function"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """Handles the 404 error"""
    output = { "error": "Not found"}
    return jsonify(output), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
