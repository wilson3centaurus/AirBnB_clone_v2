#!/usr/bin/python3
'''
    Index view for the API
'''
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


# Route that returns the status of the API
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''
        Function that returns the status of the API
    '''
    # Return the status in JSON format
    return jsonify({"status": "OK"})


# Route that retrieves the number of each objects by type
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    '''
        Function that returns the count of all objects
    '''
    classes = [Amenity, City, Place,
               Review, State, User]

    names = ["amenities", "cities",
             "places", "reviews",
             "states", "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    # Return the count of all objects in JSON format
    return jsonify(num_objs)
