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
from flasgger.utils import swag_from


@app_views.route(
    "/places/<place_id>/amenities",
    methods=['GET'],
    strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['GET'])
def list_amenities_from_place(place_id):
    """route handler to list ameinties data from place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route(
    "places/<place_id>/amenities/<amenity_id>",
    methods=['DELETE'],
    strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """route handler to delete an amenity from a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity not in place.amenities:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        place.amenities.remove(amenity)
        storage.save()
    else:
        place.amenity_ids.remove(amenity_id)
        storage.save()
    return jsonify({}), 200


@app_views.route(
    "places/<place_id>/amenities/<amenity_id>",
    methods=['POST'],
    strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['POST'])
def create_new_amenity(place_id, amenity_id):
    """route handler to post a new amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
