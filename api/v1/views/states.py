#!/usr/bin/python3
"""
Module contains all endpoints to GET, POST, PUT OR DELETE
objects from State model.
"""


from models import storage
from models.state import State
from flask import jsonify
from api.v1.views import app_views
from flask import abort
from flask import request
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route("/states", strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects.
    """
    objs = storage.all(State).values()
    states = [obj.to_dict() for obj in objs]
    return jsonify(states)


@app_views.route("/states/<id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(id):
    """
    Retrieves a State object by id.
    """
    obj = storage.get(State, id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/states/<id>", methods=["DELETE"], strict_slashes=False)
def delete_state_by_id(id):
    """
    Deletes a State object by id.
    """
    obj = storage.get(State, id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state_obj():
    """
    Creates a new State object.
    """
    try:
        body = request.get_json()
    except Exception:
        raise BadRequest("Not a JSON")

    if "name" not in body.keys():
        raise BadRequest("Missing name")
    obj = State(name=body.get("name"))
    storage.new(obj)
    storage.save()
    state = storage.get(State, obj.id)
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<id>", methods=["PUT"], strict_slashes=False)
def update_state_obj(id):
    """
    Updates a State object.
    """
    try:
        body = request.get_json()
    except Exception:
        raise BadRequest("Not a JSON")

    for key in body.keys():
        if key not in dir(State):
            msg = "Attribute {} not found in State object".format(key)
            raise BadRequest(msg)

    state_obj = storage.get(State, id)
    if state_obj is None:
        raise NotFound()

    new_name = body.get("name")
    state_obj.name = new_name
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
