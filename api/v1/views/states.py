#!/usr/bin/python3
"""
create a new view for State objects that handles all default RESTful API
actions
"""
from models import storage
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models.state import State

state_dict = storage.all('State')

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def all_states(state_id=None):
    """list of all or given state_id State Objects"""
    state_instances = [val.to_dict() for val in state_dict.values()]
    if not state_id:
        # state_instances = {keys: val.to_dict() for keys, val in state_dict.items()}
        if request.method == 'GET':
            return make_response(jsonify(state_instances), 200)
        elif request.method == 'POST':
            data = request.get_json()
            new_instance = State(**data)
            new_instance.save()
            data = storage.all("State").get("State." + new_instance.id).to_dict()
            return make_response(jsonify(data), 200)

    key = "State." + state_id
    if key in state_dict:
        if request.method == 'GET':
            return make_response(jsonify(state_dict[key].to_dict()), 200)
        elif request.method == 'DELETE':
            storage.delete(storage.all("State")[key])
            obj_inst.delete()
            return jsonify({}), 200

        elif request.method == 'PUT':
            if not request.is_json:
                abort(400)
            data = request.get_json()
            obj_inst = state_dict[key]
            for key in data.keys():
                if key != 'id' and key != 'created_at' and key != 'updated_at':
                    setattr(obj_inst, key, data[key])
            return obj_inst.to_dict()

    abort(404)

