#!/usr/bin/python3
"""This script starts the Flask web application"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})
