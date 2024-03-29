#!/usr/bin/pythin3
""" Index file. """

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

# app = Flask(__name__)

@app_views.route('/status')
def status():
    """ Function to return the status. """
    return jsonify({'Status': 'Ok'})

@app_views.route('/stats')
def stats():
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
