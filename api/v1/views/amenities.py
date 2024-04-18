#!/usr/bin/python3
"""
    This is the amenities page handler for Flask.
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """
        Flask route at /amenities.
    """
    if request.method == 'POST':
        kwargs = request.get_json()
        if not kwargs:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in kwargs:
            return jsonify({"error": "Missing name"}), 400
        new_amenity = Amenity(**kwargs)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201

    elif request.method == 'GET':
        return jsonify([amenity.to_dict() for amenity in storage.all(Amenity).values()])


@app_views.route('/amenities/<id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_id(id):
    """
        Flask route at /amenities/<id>.
    """
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)

    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        kwargs = request.get_json()
        if not kwargs:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in kwargs.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict())

    elif request.method == 'GET':
        return jsonify(amenity.to_dict())
