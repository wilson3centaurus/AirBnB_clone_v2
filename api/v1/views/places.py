#!/usr/bin/python3
'''
Places view for the API
'''

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models import storage


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places():
    places = [
        place.to_dict() for place in storage.all(Place).values()]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a specific Place object by ID """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places',
                 methods=['POST'], strict_slashes=False)
def create_place():
    """ Creates a new Place object """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Bad request: JSON data with "name" field is required')
    new_place = Place(name=data['name'])
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates an existing Place object by ID """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Bad request: JSON data is required for updating')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
