#!/usr/bin/python3
"""
creating a route /status
"""
from api.v1.views import app_views
from flask import jsonify, Flask


@app_views('/status')
def get_status():
    '''returns a JSON object'''
    return jsonify({"status": "OK"})
