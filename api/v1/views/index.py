#!/usr/bin/python3
"""
the index file
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def index():
    """ Returns status """
    return jsonify(status="OK")
