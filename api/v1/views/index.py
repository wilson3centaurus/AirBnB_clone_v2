#!/usr/bin/python3
"""Create Flask app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """returns a JSON: status: OK """
    response = {'status': "OK"}
    return jsonify(response)
