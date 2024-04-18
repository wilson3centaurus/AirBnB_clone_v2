#!/usr/bin/python3
"""defines endpoints and their output """
from api.v1.views import app_views
from flask import jsonify

# Create a route /status on the object app_views that returns a JSON: "status": "OK"
@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})
