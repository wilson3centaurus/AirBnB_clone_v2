#!/usr/bin/python3
""" states view """

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/', methods=["GET"], strict_slashes=False)
def state_get():
    """ gets states"""
    states = []
    for key, values in storage.all(State).items():
        states.append(values.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def get_state_with_id(state_id):
    """ gets state with id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=["DELETE"], strict_slashes=False)
def state_delete(state_id):
    """ deletes a state """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def state_post():
    """ creates a state """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """ updates a state """
    state = storage.get(State, state_id)
    data = request.get_json()

    if not state:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in to_ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
