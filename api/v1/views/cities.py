#!/usr/bin/python3
"""Routes for City objects"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<s_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(s_id):
    """Retrieve all cities of a state"""
    state = storage.get(State, s_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<c_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(c_id):
    """Retrieve a specific city by ID"""
    city = storage.get(City, c_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<s_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(s_id):
    """Create a new city"""
    state = storage.get(State, s_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_city = City(name=data['name'], state_id=s_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<c_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(c_id):
    """Delete a city"""
    city = storage.get(City, c_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<c_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(c_id):
    """Update a city"""
    city = storage.get(City, c_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
