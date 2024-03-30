#!/usr/bin/python
""" Basic routes """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    """
        stats of all objects route
        :return: A json representation of all objs
    """
    from models import storage
    result = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"
               }

    for cls, lab in classes.items():
        result.update({lab: storage.count(cls)})

    return jsonify(result)
