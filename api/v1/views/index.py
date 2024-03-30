#!/usr/bin/python3
"""
create Flask app, app_views
"""

from flask import jsonify, make_response, current_app
from api.v1.views import app_views


@app_views.route("/status")
def api_status():
    """returns status Ok if working"""
    response = make_response(jsonify({'status': "OK"}), 200)
    return (response)
