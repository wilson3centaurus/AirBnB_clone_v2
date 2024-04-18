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
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    elif request.method == 'GET':
        amenities = storage.all(Amenity).values()
        return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_id(id):
    """
        Flask route at /amenities/<id>.
    """
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    elif request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
