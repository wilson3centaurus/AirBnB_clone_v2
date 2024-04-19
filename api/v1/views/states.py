#!/usr/bin/python3
"""API endpoints for managing State resources."""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """Returns all State instances as JSON objects."""
    all_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def show_state(state_id):
    """Fetches a State instance by its ID, returning JSON or a 404 if not found."""
    state_instance = storage.get(State, state_id)
    if not state_instance:
        abort(404)
    return jsonify(state_instance.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def remove_state(state_id):
    """Deletes a State instance by its ID, returning a 200 JSON response on success."""
    state_to_delete = storage.get(State, state_id)
    if not state_to_delete:
        abort(404)
    state_to_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State from JSON request data, returning the new State as a JSON response."""
    state_data = request.get_json()
    if not state_data:
        abort(400, description="Not a JSON")
    if 'name' not in state_data:
        abort(400, description="Missing name")
    new_state = State(**state_data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def modify_state(state_id):
    """Updates attributes of a State instance based on JSON request data."""
    state_to_update = storage.get(State, state_id)
    if not state_to_update:
        abort(404)
    update_data = request.get_json()
    if not update_data:
        abort(400, description="Not a JSON")
    for key, value in update_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_to_update, key, value)
    state_to_update.save()
    return jsonify(state_to_update.to_dict())
