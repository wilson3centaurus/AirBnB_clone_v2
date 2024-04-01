#!/usr/bin/python3
"""module for cities api"""
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False, methods=['GET', 'POST']
                )
def cities(state_id):
    """handles creating a city and retrieving a city based on
    a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == "POST":
        request_data = request.get_json()
        if request_data:
            if "name" in request_data:
                request_data['state_id'] = state_id
                city = City(**request_data)
                city.save()
                return city.to_dict(), 201
            abort(400, "Missing name")
        abort(400, "Not a JSON")
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return cities


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def city(city_id):
    """handles retrieving, updating and deleting of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "PUT":
        request_data = request.get_json()
        if request_data:
            for key, value in request_data.items():
                if (key != "id" or key != "state_id"
                   or key != "created_at"
                   or key != "updated_at"):
                    setattr(city, key, value)
            city.save()
            return city.to_dict(), 200
        return jsonify(error="Not a JSON"), 400
    if request.method == "DELETE":
        city.delete()
        storage.save()
        return {}, 200
    city_data = {}
    for key, value in city.to_dict().items():
        if key != "state":
            city_data[key] = value
    return city_data, 200
