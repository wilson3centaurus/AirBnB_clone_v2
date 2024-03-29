#!/usr/bin/python3
"""
index file
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Jsonify status"""
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats')
def count_stats():
    '''Return the stats of the HBNB'''
    stats = {
        "amenities": count('Amenity'),
        "cities": count('City'),
        "places": count('Place'),
        "reviews": count('Review'),
        "states": count('State'),
        "users": count('User')
    }
    return jsonify(stats)
