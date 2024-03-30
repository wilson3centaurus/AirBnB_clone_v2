#!/usr/bin/python3
"""
Function to create a new view for City objects
that handles all default RESTFul API actions.
"""

from flask import Flask, abort, request, jsonify
from models import storage
from models.city import City
from api.v1.views import app_views


app_views.url_map.strict_slashes = False


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_city_by_state(s_id):
    """ Function that retrieves the list of all City objects of a State using GET. """
    state = storage.get("State", s_id)
    if state is None:
        abort(404)
    cities = [c.to_dict() for c in state.cities]
    return jsonify(cities), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_id(c_id):
    """ Function to retrieves a city and its id using GET. """
    city = storage.get("City", c_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(c_id):
    """ Function that deletes a city obj given city_id. """
    city = storage.get("City", c_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(s_id):
    """ Function that creates new city obj state using POST method. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        state = storage.get("State", s_id)
        if state is None:
            abort(404)
        obj_data['state_id'] = state.id
        obj = City(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(c_id):
    """ Function to update an existing city object using PUT. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    city_obj = storage.get("City", c_id)
    if city_obj is None:
        abort(404)
    obj_data = request.get_json()
    city_obj.name = obj_data['name']
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
