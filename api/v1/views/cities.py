#!/usr/bin/python3
""" This file contains the views implementation of
cities request as blueprint"""
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def list_cities(state_id):
    """ The list of cities for a given state id"""
    state_object = storage.get(State, state_id)
    if not state_object:
        abort(404)
    if request.method == "GET":
        cities_list = [city.to_dict() for city in state_object.cities]
        return jsonify(cities_list)
    if request.method == "POST":
        json_data = request.get_json()
        if not json_data:
            abort(400, description="Not a JSON")
        if "name" not in json_data.keys():
            abort(400, description="Missing name")
        state_object.cities.append(City(**json_data))
        storage.save()
        return make_response(jsonify(json_data), 201)


@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'])
def retrieve_city_object(city_id):
    """ Used to return city object representation"""
    city_object = storage.get(City, city_id)
    if not city_object:
        abort(404)
    if request.method == "GET":
        city_repr = city_object.to_dict()
        return jsonify(city_repr)
    if request.method == "DELETE":
        storage.delete(city_object)
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        user_data = request.get_json()
        print("User data", user_data)
        if not user_data:
            abort(400, description="Not a JSON")
        ignored_keys = ["id", "state_id", "created_at", "updated_at"]
        for key in user_data:
            if key not in ignored_keys:
                setattr(city_object, key, user_data[key])
        storage.save()
        return make_response(jsonify(city_object.to_dict()), 200)
