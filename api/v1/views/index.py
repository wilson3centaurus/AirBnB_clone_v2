#!/usr/bin/python3
'''Blueprint for /status'''


from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''Returns JSON with status'''
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = {
        Amenity: 'amenities',
        City: 'cities',
        Place: 'places',
        Review: 'reviews',
        State: 'states',
        User: 'users'
        }

    objects = {}
    for cls, value in classes.items():
        objects[value] = storage.count(cls)

    return jsonify(objects)
