#!/usr/bin/python3
"""documented module"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """retuens the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ retrieves the number of each objects by type"""
    from models import storage
    dict = {
             "amenities": storage.count(Amenity),
             "cities": storage.count(City),
             "places": storage.count(Place),
             "reviews": storage.count(Review),
             "states": storage.count(State),
             "users": storage.count(User)}
    return jsonify(dict)
