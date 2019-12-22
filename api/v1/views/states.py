#!/usr/bin/python3
from flask import request, abort, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'GET':
        list_states = []
        states = storage.all('State').values()
        for state in states:
            list_states.append(state.to_dict())
        return jsonify(list_states)

    if request.method == 'POST':
        request_json = request.get_json()
        if not isinstance(request_json, dict):
            abort(400, 'Not a JSON')
        if 'name' not in request_json:
            abort(400, 'Missing name')
        state = State(request_json)
        for key, value in request_json.items():
            if key != "__class__":
                setattr(state, key, value)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict())

@app_views.route('/states/<id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def state(id=None):
    """
    Retrieves the list of all State objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'GET':
        state = storage.get('State', id)
        if state:
            return jsonify(state.to_dict())
        abort(404)

    if request.method == 'DELETE':
        state = storage.get('State', id)
        if state:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        abort(404)

    if request.method == 'PUT':
        request_json = request.get_json()
        if not isinstance(request_json, dict):
            abort(400, error='Not a JSON')
        state = storage.get('State', id)
        if state:
            for key, value in request_json.items():
                if key not in ["__class__", "id", "created_at", "updated_at"]:
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200
        abort(404)
