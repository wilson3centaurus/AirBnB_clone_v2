#!/usr/bin/python3
""" Cities view """

from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def city_get(state_id):
    """ gets cities"""
    state = storage.get(State, state_id)
    cities = []
    if not state:
        abort(404)
    for city in state.cities:
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def get_city_with_id(city_id):
    """ gets city with id """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)

    return jsonify(cities.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def city_delete(city_id):
    """ deletes a city """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=["POST"], strict_slashes=False)
def city_post(state_id):
    """ creates a city """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """ updates a city """
    city = storage.get(City, city_id)
    data = request.get_json()

    if not city:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'created_at', 'updated_at', 'state_id']

    for key, value in data.items():
        if key not in to_ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
