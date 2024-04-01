#!/usr/bin/python3
""" Blueprint for the views """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """status"""
    return jsonify({"status": "OK"})
