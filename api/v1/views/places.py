#!/usr/bin/python3
""" View for place object """

from flask import request, abort, make_response, jsonify
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrieve all places """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_places = []
    for place in city.places:
        list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieve a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create a place """
    response = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if response is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in response:
        abort(400, 'Missing user_id')
    user = storage.get(User, response['user_id'])
    if user is None:
        abort(404)
    if 'name' not in response:
        abort(400, 'Missing name')
    response['city_id'] = city_id
    new_place = Place(**response)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in keys:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
