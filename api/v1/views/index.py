#!/usr/bin/python3
"""API routes"""

from flask import jsonify
from api.v1.views import app_views

from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def api_status():
    """Return a JSON"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", stricy_slashes=False)
def get_stats():
    '''Retrieves the number of each objects by type'''
    return jsonfy({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Places),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })
