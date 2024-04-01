#!/usr/bin/python3
"""
creating a route /status
"""
from api.v1.views import app_views
from flask import jsonify, Flask
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    '''returns a JSON object'''
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def get_object():
    '''retrieves the number of ech objects by type'''
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")
                    })

