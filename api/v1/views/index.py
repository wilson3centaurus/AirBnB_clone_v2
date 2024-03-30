#!/usr/bin/python3
"""Contains index view for API"""

from flask import Flask, request, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


# Define a route / status on the object app_views
@app_views.route('/status')
def get_status():
    """Gets the status code of the API"""
    return jsonify(status ="OK")
@app_views.route('/stats'):
def get_stats():
    """Gets the number of objects form storage model"""
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)