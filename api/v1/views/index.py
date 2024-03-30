#!/usr/bin/python3
"""
index - status OK
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns server status"""
    return jsonify({"status": "OK"})
