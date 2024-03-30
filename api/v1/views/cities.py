#!/usr/bin/python3
"""
State view
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id=None):
    """Get state object"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)

    allCity = storage.all('City')
    cities_by_state = [obj.to_dict() for obj in allCity.values()
                       if obj.state_id == state_id]
    return jsonify(cities_by_state)


@app_views.route('cities/<city_id>', methods=['GET'])
def get_cities(city_id=None):
    """Get state object based on ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'])
def Del_city(city_id=None):
    """Get state object based on ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    del city
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_cities_by_state(state_id=None):
    """Get state object"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get("name") is None:
        abort(400, 'Missing name')
    req_json['state_id'] = state_id
    new_city = City(**req_json)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'])
def put_city(city_id=None):
    """Get state object based on ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    for key, value in req_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
