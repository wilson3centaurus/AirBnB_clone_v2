#!/usr/bin/python3
"""
creating a view for Amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    '''RETRIEVE THE LIST OF ALL Amenity OBJECTS'''
    obj_lst = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(obj_lst)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    '''retrive a amenity object by its id'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''delete a amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
    else:
        abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    '''create a amenity object'''
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state_data = request.get_json()
    amenity = Amenity(**state_data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''update a amenity by its id'''
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json()
    if not request.get_json():
        abort(400, 'Not a JSON')
    if amenity:
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
    else:
        abort(404)
    storage.save()
    return jsonify(amenity.to_dict()), 200
