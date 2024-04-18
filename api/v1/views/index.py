#!/usr/bin/python3
"""

"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def return_status():
    """Returns app_views object status as a JSON file"""
    return jsonify({"status": "OK"})
