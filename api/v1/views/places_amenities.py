#!/usr/bin/python3
"""
view for the link between Place objects
and Amenity objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from os import environ


@app_views.route(
    "/places/<place_id>/amenities",
    methods=['GET'],
    strict_slashes=False)
def list_amenities_from_place(place_id):
    """route handler to list ameinties data from place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if environ.get('HBHB_TYPE_STORAGE') == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route(
    "places/<place_id>/amenities/<amenity_id>",
    methods=['DELETE'],
    strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """route handler to delete an amenity from a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)

    if environ.get('HBHB_TYPE_STORAGE') == 'DBStorage':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
    else:
        if amenity not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save()
    return jsonify({}), 200


@app_views.route(
    "places/<place_id>/amenities/<amenity_id>",
    methods=['POST'],
    strict_slashes=False)
def create_new_amenity(place_id, amenity_id):
    """route handler to post a new amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)

    if environ.get('HBHB_TYPE_STORAGE') == 'DBStorage':
        if amenity not in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
    else:
        if amenity not in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save()
    return jsonify(amenity.to_dict()), 201
