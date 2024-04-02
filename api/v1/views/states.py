#!/usr/bin/python3
"""
Perform REst API ACtions to state
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request
from flask import abort


@app_views.route('/states/', methods=['GET'])
def all_states():
    """listing all states in storage"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'])
def state_by_id(state_id):
    """retreiving state by id"""
    state = storage.all()
    for key, val in state.items():
        if val.to_dict().get('id') == state_id:
            return jsonify(val.to_dict())
    return (abort(404))


@app_views.route('/states/', methods=['POST'])
def post_state():
    """creating a new State"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update state by id"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    states = storage.all(State)
    all_dict = {}
    for k, v in states.items():
        if v.to_dict().get('id') == state_id:
            state = v
    for j, m in data.items():
        setattr(state, j, m)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deleting a state by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)  # State not found

    storage.delete(state)
    storage.save()
    return jsonify({}), 200
