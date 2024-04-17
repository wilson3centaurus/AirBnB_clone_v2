#!/usr/bin/python3ù
""" returns json statuses for app_views routes"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns status OK"""
    return jsonify({"status": "OK"})
