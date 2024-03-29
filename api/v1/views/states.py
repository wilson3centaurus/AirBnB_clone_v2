#!/usr/bin/python3
"""View for state objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def view_states():
    """Returns a list containing all State objects"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state object"""
    if not request.json:
        raise abort(400, description="Not a JSON")
    if 'name' not in request.json:
        raise abort(400, description="Missing name")
    state_data = request.get_json()
    new_state = State(name=state_data['name'])
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False)
def view_state(state_id):
    """Returns the state with id 'state_id'"""
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['PUT', 'PATCH'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates the state with id 'state_id'"""
    if not request.json:
        raise abort(400, description="Not a JSON")
    for state in storage.all(State).values():
        if state.id == state_id:
            state_dict = request.get_json()
            for k, v in state_dict.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(state, k, v)
            state.save()
            return jsonify(state.to_dict()), 200
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes the state with id 'state_id'"""
    for state in storage.all(State).values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    abort(404)
