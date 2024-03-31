#!/usr/bin/python3
"""API routes"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def api_status():
    """Return a JSON"""
    return jsonify({"status": "OK"})
