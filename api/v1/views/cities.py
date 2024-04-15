#!/usr/bin/python3
"""API endpoints for City resource management."""
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def list_cities(state_id):

    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
def show_city(city_id):
    """Retrieves a specific city by its ID."""
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
def remove_city(city_id):

    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def add_city(state_id):

    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")
    city_data = request.get_json()
    if not city_data:
        abort(400, description="Request body must be JSON")
    if 'name' not in city_data:
        abort(400, description="Missing 'name' in request data")
    new_city = City(state_id=state_id, **city_data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def edit_city(city_id):

    city = storage.get(City, city_id)
    if not city:
        abort(404, description="City not found")
    update_data = request.get_json()
    if not update_data:
        abort(400, description="Request body must be JSON")
    for key, value in update_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
