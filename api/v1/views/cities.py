#!/usr/bin/python3
"""
Module that handles:
    - Retrieval of list of all City objects of a State.
    - Retrieval of a City object.
    - Deletion of a City object.
    - Creation of a City.
    - Updates a City object
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/api/v1/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects of a State
    Parameters:
        state_id: uuid for the state object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/api/v1/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a city object
    Parameters:
        city_id: uuid for city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route('/api/v1/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a City """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")

    dataset = request.get_json()
    dataset['state_id'] = state_id
    city = City(**dataset)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")

    dataset = request.get_json()
    for key, value in dataset.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200
