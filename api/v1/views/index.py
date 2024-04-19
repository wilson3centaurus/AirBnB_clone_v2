#!/usr/bin/python3
""" Module containing all routes belonging to app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def index():
    """
    returns a JSON message
    """
    message = {"status": "OK"}
    return jsonify(message)
