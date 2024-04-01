#!/usr/bin/python3
"""
creating a view for City objects
"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.city import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def cities():
    '''RETRIEVE THE LIST OF ALL CITY OBJECTS'''
    obj_lst = [obj.to_dict() for obj in storage.all(City).values()]
    return jsonify(obj_lst)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(city_id):
    '''retrive a city object by its id'''
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(city_id):
    '''delete a city object'''
    city = storage.get(City, city_id)
    if city:
        city.delete()
    else:
        abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities', methods=['POST'],
                 strict_slashes=False)
def create_state():
    '''create a city object'''
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state_data = request.get_json()
    city = City(**state_data)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(city_id):
    '''update a city by its id'''
    city = storage.get(City, city_id)
    data = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    if city:
        for key, value in data.items():
            if key not in ['id', 'creates_at', 'updated_at']:
                setattr(city, key, value)
    else:
        abort(404)
    storage.save()
    return jsonify(city.to_dict()), 200
