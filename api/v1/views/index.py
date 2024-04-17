#!/usr/bin/python3
"""
Module for the API.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Status of the API"""

    return jsonify({"status": "OK"})
