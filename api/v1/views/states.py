#!/usr/bin/python3
"""
Handles State objects
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, State
from models.state import State

# Endpoint to retrieve the list of all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    # Retrieve all State objects from storage and convert them to dictionaries
    states = [state.to_dict() for state in storage.all(State).values()]
    # Return the list of State dictionaries as JSON response
    return jsonify(states)


# Endpoint to retrieve a specific State object by its ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    # Retrieve the State object with the given state_id from storage
    state = storage.get(State, state_id)
    # If State object is not found, return 404 error
    if state is None:
        abort(404)
    # Return the State object as JSON response
    return jsonify(state.to_dict())


# Endpoint to delete a specific State object by its ID
@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    # Retrieve the State object with the given state_id from storage
    state = storage.get(State, state_id)
    # If State object is not found, return 404 error
    if state is None:
        abort(404)
    # Delete the State object from storage
    storage.delete(state)
    # Commit the changes to the storage
    storage.save()
    # Return an empty JSON response with HTTP status code 200
    return jsonify({}), 200
