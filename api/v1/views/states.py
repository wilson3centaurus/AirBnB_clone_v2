#!/usr/bin/python3
'''
    State module for the API
'''
from flask import abort, jsonify, request
from .index import app_views
from models import storage
from models.state import State


# Route that returns a JSON response with all State objects
@app_views.route('/states',
                 methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    '''
        Get a state object by ID or all state objects if no ID is given
    '''
    if state_id is None:
        states = storage.all(State).values()
        # Return a JSON response with all State objects
        return jsonify([state.to_dict() for state in states])
    else:
        state = storage.get(State, state_id)
        # If the state object was found
        if state:
            # Return the State object with a status of 200
            return jsonify(state.to_dict())
        else:
            # Return a 404 error if the state object was not found
            abort(404)


# Route that deletes a State object by ID
@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''
        Delete a state object by ID
    '''
    state = storage.get(State, state_id)

    # If the state object was found
    if state:
        # Delete the State object and return an empty dictionary with status
        storage.delete(state)
        storage.save()

        # Return an empty dictionary with a status of 200
        return jsonify({}), 200
    else:
        # Return a 404 error if the state object was not found
        abort(404)


# Route that creates a State object
@app_views.route('/states',
                 methods=['POST'], strict_slashes=False)
def create_state():
    '''
        Create a new state object
    '''
    # If the request is not in JSON format
    if not request.get_json():
        abort(400, description='Not a JSON')

    # Get the JSON request
    data = request.get_json()

    # If the JSON request does not contain the key 'name'
    if 'name' not in data:
        # Return a 400 error with a message
        abort(400,
              description='Missing name')

    # Create a new State object with the JSON request data
    new_state = State(**data)
    new_state.save()

    # Return the new State object with a status of 201
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    '''
        Update a state object
    '''
    state = storage.get(State, state_id)

    # If the state object was not found
    if not state:
        # Return a 404 error
        abort(404)

    # If the request is not in JSON format
    if not request.get_json():
        # Return a 400 error
        abort(400,
              description="Not a JSON")

    # Get the JSON request
    skip_keys = ['id', 'created_at',
                 'updated_at']

    data = request.get_json()

    # Update the state object with the JSON request data
    for key, value in data.items():
        if key not in skip_keys:
            # Set the attribute
            setattr(state, key, value)
    storage.save()

    # Return the state object with a status of 200
    return jsonify(state.to_dict()), 200
