#!/usr/bin/python3
"""State view"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """Get all states"""
    return jsonify(storage.all(State))


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Get state based on state_id"""
    try:
        return jsonify(storage.get(State, state_id).to_dict())
    except Exception as e:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a State"""
    try:
        state = storage.get(State, state_id)
        storage.delete(state)
        return jsonify({}), 200
    except Exception as e:
        abort(404)


@app_views.route('/states', methods=['POST'])
def post_state():
    """Creates a State object"""
    ## get the dict from the request {name}
    ## check if dict is valid
    ## return new state with 201
    req = request.get_json()
    if req:
        if "name" in req.keys():
            state = State(req["name"])
            storage.new(state)
            return jsonify(state), 201
        else:
            return "Missing name", 400
    else:
        return "Not a JSON", 400


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """Updates a State object"""
    try:
        state = storage.get(State, state_id)
    except Exception as e:
        abort(404)
    req = request.get_json()
    if req:
        state.name = req["name"]
        ## I might need to state.save() here
        return jsonify(state), 200
    else:
        return "Not a JSON", 400


if __name__ == '__main__':
    pass
