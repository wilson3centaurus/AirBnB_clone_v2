#!/usr/bin/python3
"""
create Flask app, app_views
"""

from flask import jsonify
from api.vi.views import app_views

@app_views.route("/status")
def api_status():
    """
    """
    response = {"status": "OK"}
    return jsonify(response)
