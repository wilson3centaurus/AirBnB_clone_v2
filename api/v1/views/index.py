#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User

obj_dict = {'amenities': Amenity,
            'cities': City,
            'states': State,
            'places': Place,
            'reviews': Review,
            'users': User}


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({'status': 'OK'})

@app_views.route('/stats', strict_slashes=False)
def stats():
    json_result = {}
    for key, value in obj_dict.items():
        json_result[key] = storage.count(value)
    return jsonify(json_result)
