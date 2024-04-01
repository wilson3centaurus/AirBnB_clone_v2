#!/usr/bin/python3
"""index.py module
"""
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def index():
    """index view"""
    return jsonify(status="OK")

@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    retrieves the number of each objects by type
    """
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    count = {}
    for key, value in classes.items():
        count[key] = storage.count(value)
    return jsonify(count)

