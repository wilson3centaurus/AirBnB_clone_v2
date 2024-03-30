#!/usr/bin/python3
""" The view for Place objects that handles all default RESTFul API actions. """

from flask import Flask, abort, request, jsonify
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_place_by_city(c_id):
    """ Function that retrieves the list of all Place objects of a City:
        GET /api/v1/cities/<city_id>/places. """
    city = storage.get("City", c_id)
    if city is None:
        abort(404)
    places = [p.to_dict() for p in city.places]

    return jsonify(places), 200


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_id(p_id):
    """ Function retrieves a Place object:
        GET /api/v1/places/<place_id>. """
    place = storage.get("Place", p_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(p_id):
    """ Function that deletes a Place object:
        DELETE /api/v1/places/<place_id>. """
    place = storage.get("Place", p_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Function that creates a Place:
        POST /api/v1/cities/<city_id>/places. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    else:
        obj_data = request.get_json()
        city_obj = storage.get("City", city_id)
        user_obj = storage.get("User", obj_data['user_id'])
        if city_obj is None or user_obj is None:
            abort(404)
        obj_data['city_id'] = city_obj.id
        obj_data['user_id'] = user_obj.id
        place_obj = Place(**obj_data)
        place_obj.save()

        return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(p_id):
    """ FUnction that updates a Place object:
    PUT /api/v1/places/<place_id>. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    place_obj = storage.get("Place", p_id)
    if place_obj is None:
        abort(404)
    obj_data = request.get_json()
    ignore = ("id", "user_id", "created_at", "updated_at")
    for k, v in obj_data.items():
        if k not in ignore:
            setattr(place_obj, k, v)
    place_obj.save()

    return jsonify(place_obj.to_dict()), 200
