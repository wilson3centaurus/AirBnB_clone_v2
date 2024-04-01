#!/usr/bin/python3
'''View for State objs that handles all default RESTFul API actions'''

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    '''Retrieves the list of all State objs'''
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    '''Retrieves a State obj'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state = state.to_dict()
    return jsonify(state)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_state(state_id):
    '''Deletes a State obj'''
    emp_dict = {}
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify(emp_dict), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    '''Creates a State'''
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    state = state.to_dict()
    return jsonify(state), 201


@app_views.route('/states/<state_id>', methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id):
    '''Updates a State obj'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    skeys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in skeys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
