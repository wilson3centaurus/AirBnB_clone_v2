#!/usr/bin/python3
"""
    Cities_view routes C.R.U.D methods
"""
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
        Retrieve all City objects linked to a State.
        Args:
            state_id (str): The ID of the State.
        Returns:
            JSON: A JSON response containing dictionaries of the City objects.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
        Retrieve a City object by ID.
        Args:
            city_id (str): The ID of the City.
        Returns:
            JSON: A JSON response containing the City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
        Delete a City object by ID.
        Args:
            city_id (str): The ID of the City.
        Returns:
            JSON: An empty JSON response with a status code of 200.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
        Create a City object linked to a State.
        Args:
            state_id (str): The ID of the State.
        Returns:
            JSON: A JSON response containing the new City object.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
        Update a City object by ID.
        Args:
            city_id (str): The ID of the City.
        Returns:
            JSON: A JSON response containing the updated City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
