#!/usr/bin/python3
"""
This file contains views for the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ get amenities all amenities """
    all_amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return make_response(jsonify(all_amenities), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ gets amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """ create a new amenity """
    if not request.is_json and not request.get_json().get('name', None):
        abort(400)
    js = request.get_json()
    obj = Amenity(**js)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ udates an amentiy instance """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    if not request.is_json and not request.get_json().get('name', None):
        abort(400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
