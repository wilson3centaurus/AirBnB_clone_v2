#!/usr/bin/python3
"""API endpoints for Amenity resource management."""
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """Returns all Amenity objects as JSON."""
    all_amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'], strict_slashes=False)
def show_amenity(amenity_id):
    """Retrieves a specific Amenity by its ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'], strict_slashes=False)
def remove_amenity(amenity_id):
    """Deletes an Amenity using its ID and returns a 200 response."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """Creates a new Amenity from JSON request data."""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, description="Not a JSON")
    if 'name' not in amenity_data:
        abort(400, description="Missing 'name'")
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'], strict_slashes=False)
def edit_amenity(amenity_id):
    """Updates an existing Amenity with new data provided in JSON format."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    update_data = request.get_json()
    if not update_data:
        abort(400, description="Not a JSON")
    for key, value in update_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
