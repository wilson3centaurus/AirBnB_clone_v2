#!/usr/bin/python3
"""
Module for the API.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Status of the API"""

    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    return {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('Cities'),
        "places": storage.count('Places'),
        "reviews": storage.count('Reviews'),
        "states": storage.count('States'),
        "users": storage.count('Users')
    }
