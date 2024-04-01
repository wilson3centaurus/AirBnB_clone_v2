#!/usr/bin/python3
"""handles amenities request"""
from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def amenities():
    """handles getting all amenities and creating amenities"""
    if request.method == "POST":
        request_data = request.get_json()
        if request_data:
            if "name" in request_data:
                amenity = Amenity(**request_data)
                amenity.save()
                return amenity.to_dict(), 201
            abort(400, "Missing name")
        abort(400, "Not a JSON")
    all_amenities = []
    for amenity in storage.get_all(Amenity):
        all_amenities.append(amenity.to_dict())
    return all_amenities


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def retrieve_delete_update(amenity_id):
    """retrieve, delete and update and amenity based on id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == "PUT":
        request_data = request.get_json()
        if request_data:
            for key, value in request_data.items():
                if key not in ["id", "updated_at", "created_at"]:
                    setattr(amenity, key, value)
            amenity.save()
            return amenity.to_dict(), 200
    if request.method == "DELETE":
        amenity.delete()
        storage.save()
        return {}, 200
    return amenity.to_dict(), 200
