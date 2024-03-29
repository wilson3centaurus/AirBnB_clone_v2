#!/usr/bin/python3
""" Index file for the Flask's general routes. """

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """ Function to return the status. """
    return jsonify({"status": "Ok"})


@app_views.route('/stats')
def stats():
    """ Function to return number objects in a storage. """
    for obj in storage.all():
        object_counts = {
                "amenities": storage.count('Amenity'),
                "cities": storage.count('City'),
                "places": storage.count('Place'),
                "reviews": storage.count('Review'),
                "states": storage.count('State'),
                "users": storage.cout('Users')
                }
        return jsonify(object_counts)
