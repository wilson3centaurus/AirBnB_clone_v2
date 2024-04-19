#!/usr/bin/python3
'''
Amenities view for the API
'''

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a specific Amenity object by ID """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a specific Amenity object by ID """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a new Amenity object """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Bad request: JSON data with "name" field is required')
    new_amenity = Amenity(name=data['name'])
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an existing Amenity object by ID """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        abort(400, 'Bad request: JSON data is required for updating')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
