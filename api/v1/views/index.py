#!/usr/bin/python3
"""index file to run the flask app"""
from flask import jsonify

from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """Status route"""
    return jsonify({"status": "OK"})
