#!/usr/bin/python3
"""
Here is where we create the routes to the endpoints of our blueprints
"""

from flask import jsonify, request
from models import storage
# we import the Blueprint 'app_views'created in the __init__
from api.v1.views import app_views


# the followings are the entendpoints of the app_view blueprint
# in other words /status == /api/v1/status and /stats == /api/v1/stats
# we create that blueprint to access to all the endpoints easily

@app_views.route('/status', methods=['GET'])
def status():
    """ returns status """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    function to return the count of all class objects
    """
    if request.method == 'GET':
        response = {}
        classes = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in classes.items():
            response[value] = storage.count(key)
        return jsonify(response)
