#!usr/bin/python3
""" Amenities View """

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities/', methods=["GET"], strict_slashes=False)
def amenities_get():
    """ gets amenities """
    amenities = []
    for key, values in storage.all(Amenity).items():
        amenities.append(values.to_dict())

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=["GET"], strict_slashes=False)
def get_amenity_with_id(amenity_id):
    """ gets amenity with id """
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)

    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenities_id>',
                 methods=["DELETE"], strict_slashes=False)
def amenities_delete(amenity_id):
    """ deletes an amenity """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def amenity_post():
    """ creates an amenity """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=["PUT"], strict_slashes=False)
def amenities_put(amenity_id):
    """ updates an amenity """
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json()

    if not amenity:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in to_ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
