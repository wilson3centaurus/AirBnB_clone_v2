#!/usr/bin/python3
""" A view to handle RESTful API for class Amenity. """

from flask import Flask, abort, request, jsonify
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


app_views.url_map.strict_slashes = False


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """ Function to retrieves the list of all Amenity objects. """
    amenities = [am.to_dict() for am in storage.all('Amenity').values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_id(am_id):
    """ Function to retrieves a Amenity object. """
    amenity = storage.get("Amenity", am_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(am_id):
    """ Function deletes a Amenity object. """
    amenity = storage.get("Amenity", am_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenities():
    """ Function to creates a new Amenity object. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        am_obj = Amenity(**obj_data)
        am_obj.save()
        return jsonify(am_obj.to_dict()), 201


@app_views.route('/amenities/<amenities_id>', methods=['PUT'])
def update_amenity(am_id):
    """ Function that updates an Amenity object. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    am_obj = storage.get("Amenity", am_id)
    if am_obj is None:
        abort(404)
    obj_data = request.get_json()
    am_obj.name = obj_data['name']
    am_obj.save()
    return jsonify(am_obj.to_dict()), 200
