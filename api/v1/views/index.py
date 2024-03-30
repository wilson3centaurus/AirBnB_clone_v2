#!/usr/bin/python3
"""
    Module implementing routes for our api

"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """returns http status code"""
    return jsonify({'status': 'OK'})
