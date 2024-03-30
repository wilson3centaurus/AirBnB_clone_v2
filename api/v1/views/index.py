#!/usr/bin/python3
"""index module"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """return status"""
    status = {
        "status": "OK"
    }
    response = jsonify(status)
    response.status_code = 200
    return response
