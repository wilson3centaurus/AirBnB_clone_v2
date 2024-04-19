#!/usr/bin/python3
'''
Cities view for the API
'''

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models import storage


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    cities = [
        city.to_dict() for city in storage.all(City).values()]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a specific City object by ID """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities',
                 methods=['POST'], strict_slashes=False)
def create_city():
    """ Creates a new City object """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Bad request: JSON data with "name" field is required')
    new_city = City(name=data['name'])
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates an existing City object by ID """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Bad request: JSON data is required for updating')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
