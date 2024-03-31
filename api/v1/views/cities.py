#!/usr/bin/python3
"""new view for City objects that handles RESTFul API"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_view.route("/cities/<city_id>", methods=["DELETE"],
                strict_slash=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_view.route("/states/<state_id>/cities", methods=["POST"],
                strict_slash=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_view.route("cities/<city_id>", methods=["PUT"],
                strict_slash=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
