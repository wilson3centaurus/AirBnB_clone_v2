#!/usr/bin/python3
""" Defines the routes for the API status endpoint """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def get_status():
    """ Returns a Json response indicating the status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """ Retrieves the count of existing objects by type """

    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }
    stats = {}

    for k, v in classes.items():
        stats[k] = storage.count(v)

    return jsonify(stats)
