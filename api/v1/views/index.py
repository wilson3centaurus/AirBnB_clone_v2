#!/usr/bin/python3
"""Index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Retrns a JSON"""
    return jsonify(status="OK")


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """
    Retrieves the number of each object
    by type.
    """
    """ 
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
    """
    # importing classes
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    # look up dict
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    # empty dict to fill using the method
    number_of_classes = {}
    for name, cls in classes.items():
        number_of_classes.update({name: storage.count(cls.__name__)})
    # return (json.dumps(number_of_classes, indent=2),
    #        {"Content-Type": "application/json"})
    return jsonify(number_of_classes)
