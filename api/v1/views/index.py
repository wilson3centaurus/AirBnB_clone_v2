#!/usr/bin/python3
""""""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


if __name__ == "__main__":
    pass  # Add any additional logic if required


@app_views.route('/status', method=['GET'], strict_slashes=False)
def status():
    """endpoint that returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Endpoint to retrieve stats of objects by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    print("Status:", stats)
    return jsonify(stats)
