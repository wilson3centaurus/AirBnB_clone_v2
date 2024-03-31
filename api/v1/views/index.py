#!/usr/bin/python3
"""
index
"""

from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.route('/status')
def api_status():
    """
    status route
    :return: response with json
    """
    response = {'status': "OK"}
    return jsonify(response)