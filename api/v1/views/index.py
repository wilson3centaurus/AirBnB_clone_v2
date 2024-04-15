#!/usr/bin/python3
"""API endpoints for general system status and statistics."""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def system_status():
    """Returns the current status of the system as JSON."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def object_statistics():
    """Returns a count of each object type in the system."""
    object_types = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    stats = {object_type: storage.count(cls)
             for object_type, cls in object_types.items()}
    return jsonify(stats)


if __name__ == "__main__":
    pass  # This can be used for additional configurations or tests.
