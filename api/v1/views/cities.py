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
    cities_by_state = [obj.to_json() for obj in allCity.values()
                       if obj.state_id == state_id]
    return jsonify(cities_by_state)


@app_views.route('cities/<city_id>', methods=['GET'])
def get_cities(city_id=None):
    """Get state object based on ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())


@app_views.route('cities/<city_id>', methods=['DELETE'])
def Del_city(city_id=None):
    """Get state object based on ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    del city
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_cities_by_state(state_id=None):
    """Get state object"""
    # state_by_id = storage.get(State, state_id)
    # if state_by_id is None:
    #     abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get("name") is None:
        abort(400, 'Missing name')
    req_json['state_id'] = state_id
    city = City(**req_json)
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
    city.bm_update(req_json)
    return jsonify(city.to_json()), 200


# @app_views.route('/states/<state_id>', methods=['DELETE'])
# def delete_state(state_id):
#     """Delete state object based on ID"""
#     state = storage.get(State, state_id)
#     if state:
#         storage.delete(state)
#         storage.save()
#         return jsonify({}), 200
#     else:
#         return jsonify({'error': 'Not found'}), 404


# @app_views.route('/states/', methods=['POST'])
# def create_state():
#     """Creates new state"""
#     data = request.get_json()
#     if data is None:
#         return jsonify({'error': 'Not a JSON'}), 400
#     if 'name' not in data:
#         return jsonify({'error': 'Missing name'}), 400

#     new_state = State(**data)
#     new_state.save()

#     return jsonify(new_state.to_dict()), 201


# @app_views.route('/states/<state_id>', methods=['PUT'])
# def update_state(state_id):
#     """Update a State"""
#     state = storage.get(State, state_id)
#     if not state:
#         return jsonify({'error': 'Not found'}), 404

#     data = request.get_json()
#     if data is None:
#         return jsonify({'error': 'Not a JSON'}), 400

#     # Remove keys to be ignored
#     data.pop('id', None)
#     data.pop('created_at', None)
#     data.pop('updated_at', None)

#     # Update state object with new data
#     for key, value in data.items():
#         setattr(state, key, value)

#     state.save()
#     return jsonify(state.to_dict()), 200
