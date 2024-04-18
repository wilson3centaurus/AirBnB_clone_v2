#!/usr/bin/python3
"""
    This is the cities page handler for Flask.
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.city import City
from models.state import State


@app_views.route('/states/<id>/cities', methods=['GET', 'POST'])
def states_id_cities(id):
    """
        Flask route at /states/<id>/cities.
    """
    state = storage.get(State, id)
    if not state:
        abort(404)

    if request.method == 'POST':
        kwargs = request.get_json()
        if not kwargs:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in kwargs:
            return jsonify({"error": "Missing name"}), 400
        new_city = City(state_id=id, **kwargs)
        new_city.save()
        return jsonify(new_city.to_dict()), 201

    elif request.method == 'GET':
        return jsonify([c.to_dict() for c in state.cities])
    