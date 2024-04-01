#!/usr/bin/python3
""" Blueprint for the views """

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """status"""
    return jsonify({"status": "OK"})
