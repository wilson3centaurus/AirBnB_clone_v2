#!/usr/bin/python3
"""Creates Flask app"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """
    Returns a JSON with the status
    """
    response = {'status': "OK"}
    return jsonify(response)
