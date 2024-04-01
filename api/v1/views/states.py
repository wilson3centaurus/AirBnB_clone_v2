#!/usr/bin/python3
"""
states module for the API v1
"""
from flask import abort, request, jsonify
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states():
    """retrieves the list of all States"""
    if request.method == "POST":
        request_data = request.get_json()
        if request_data:
            if request_data.get('name'):
                state = State(**request_data)
                state.save()
                return (state.to_dict(), 201)
            else:
                response = jsonify({'error': 'Missing name'})
                response.status_code = 400
                return response
        else:
            response = jsonify({'error': 'Not a JSON'})
            response.status_code = 400
            return response
    states = []
    all_states = storage.get_all(State)
    for state in all_states:
        states.append(state.to_dict())
    return states


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['GET', 'PUT'])
def state(state_id):
    """retrieves and update a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == "PUT":
        request_data = request.get_json()
        if request_data:
            for key, value in request_data.items():
                if key != "id" or key != "updated_at" or key != "created_at":
                    setattr(state, key, value)
            state.save()
            return state.to_dict(), 200
        response = jsonify(error="Not a JSON")
        return response
    return state.to_dict()


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """Deletes a states with a valid id"""
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return {}, 200
    abort(404)
