#!/usr/bin/python3
"""
view for the link between Place objects
and Amenity objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from models import amenity
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
    "/places/<place_id>/amenity",
    method=['GET'],
    strict_slashes=False)
def list_amenities_from_place(place_id):
    """route handler to list ameinties data from place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        amenities = [Amenity.to_dict() for Amenity in place.amenities]
    else:
        amenities = [storage.get(amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route(
    "places/<place_id>/amenities/<amenity_id>",
    method=['DELETE'],
    strict_slashe=False)
def delete_amenity(place_id, amenity_id):
    """route handler to delete an amenity from a place"""
    place = storage.get(Place, place_id)
    Amenity = storage.get(amenity, amenity_id)
    if place is None:
        abort(404)
    elif Amenity is None or Amenity not in place.amenities:
        abort(404)
    if storage.__class__.__name__ == 'DBStorage':
        place.amenities.remove(Amenity)
        storage.save()
    else:
        place.amenity_ids.remove(amenity_id)
        storage.save()
    return jsonify({}), 200


@app_views.route(
    "places/<place_id>/amenities/<amenity_id>",
    method=['POST'],
    strict_slashe=False)
def create_new_amenity(place_id, amenity_id):
    """route handler to post a new amenity"""
    place = storage.get(Place, place_id)
    Amenity = storage.get(amenity, amenity_id)
    if place is None or Amenity:
        abort(404)
    if Amenity in place.amenities:
        return jsonify(Amenity.to_dict()), 200
    
    place.amenities.append(Amenity)
    storage.save()
    return jsonify(Amenity.to_dict()), 201
