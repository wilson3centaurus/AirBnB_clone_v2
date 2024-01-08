#!/usr/bin/python3
"""this module handles all default RESTFul API actions"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def create_state():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def update_state(state_id):
    """
    updates a state give a valid id
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    state = storage.get(State, state_id)
    if state is None:
        abort(400)

    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
