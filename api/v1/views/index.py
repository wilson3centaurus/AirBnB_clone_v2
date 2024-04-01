#!/usr/bin/python3
"""Endpoints for stats"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieve statistics for various object types"""
    count_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(count_dict)

