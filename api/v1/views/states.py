from flask import make_response, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def all_states(state_id=None):
    if state_id:
        state_instance = storage.get(State, state_id)
        if not state_instance:
            abort(404)

    if request.method == 'GET':
        if state_id:
            return jsonify(state_instance.to_dict()), 200
        else:
            state_inst = [val.to_dict() for val in storage.all(State).values()]
            return jsonify(state_inst), 200

    elif request.method == 'POST':
        if not request.is_json:
            abort(400)
        data = request.get_json()
        if "name" not in data:
            abort(400, description="Missing 'name' in request JSON")
        new_instance = State(**data)
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201

    elif request.method == 'DELETE':
        storage.delete(state_instance)
        storage.save()
        return jsonify({}), 204

    elif request.method == 'PUT':
        if not request.is_json:
            abort(400)
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state_instance, key, value)
        storage.save()
        return jsonify(state_instance.to_dict()), 200
