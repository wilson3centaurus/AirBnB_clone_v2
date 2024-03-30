#!/usr/bin/python3
"""
Module that handles:
    - Retrieval of list of all Amenities objects of a Place.
    - Retrieval of a Amenities object.
    - Deletion of a Amenities object.
    - Creation of a Amenities.
    - Updates a Amenities object.
"""


from flask import jsonify, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'])
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    Args:
        place_id: uuid for the place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object from a Place
    Args:
        place_id: uuid for the place object
        amenity_id: uuid for the amenity object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place
    Args:
        place_id: uuid for the place object
        amenity_id: uuid for the amenity object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201
