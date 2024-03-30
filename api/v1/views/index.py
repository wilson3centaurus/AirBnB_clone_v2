#!/usr/bin/python3
"""Contains the index view for the API."""
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# No need to import app_views at the top

# Define a route / status on the object app_views
def get_status():
    """Gets the status code of the API"""
    from api.v1.views import app_views  # Import inside the function
    return jsonify(status="OK")


# Define a route / stats on the object app_views
def get_stats():
    """Gets the number of objects from storage model"""
    from api.v1.views import app_views  # Import inside the function
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
