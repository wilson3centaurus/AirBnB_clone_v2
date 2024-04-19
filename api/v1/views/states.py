#!/usr/bin/python3
"""
    States_views routes C.R.U.D methods
"""
from flask import jsonify, abort, request
from .index import app_views
from models.state import State
from models import storage
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """
        Retrieve all State objects or a single State
        if ID is provided '/states/<state_id>'

        Returns:
        JSON: A JSON response containing dictionaries of the object(s).
    """
    if state_id is None:
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])
    else:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        else:
            abort(404)


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_state(state_id):
    """
    Delete a State object by ID.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        JSON: An empty JSON response with a status code of 200
        if the deletion is successful.
            Otherwise, a 404 error is raised if the State object is not found.
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        # Return a 404 error if State object not found
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a State object based on the body from the request

    Returns:
        JSON:
    """
    # Not valid json data
    if not request.get_json():
        abort(400, description='Not a JSON')

    # Get json, must have {'name': <name_of_state>}
    data = request.get_json()

    if 'name' not in data:
        abort(400, description='Missing name')

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Update a State object.

    Args:
        state_id (str): The ID of the State object to update.

    Returns:
        JSON: A JSON response containing the updated State object if success
              or an appropriate error response if the update fails.
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    skip_keys = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in skip_keys:
            # Here we are updating the values
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
