#!/usr/bin/python3
"""
State view
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def get_state():
    """Get state object"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    """Get state object based on ID"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete state object based on ID"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Creates new state"""
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a State"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    # Remove keys to be ignored
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)

    # Update state object with new data
    for key, value in data.items():
        setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
