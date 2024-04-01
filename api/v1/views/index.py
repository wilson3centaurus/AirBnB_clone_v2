#!/usr/bin/python3
"""
creating a route /status
"""
from . import app_views
from flask import jsonify


@app_views('/status')
def get_status():
    '''returns a JSON object'''
    return jsonify({"status": "OK"})
