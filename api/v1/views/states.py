#!/usr/bin/python3
"""State"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route("/states", methods=["GET"])
def states_all():
    """Retrieves all states with a list of objects"""
    lists = []
    s = storage.all('State').values()
    for v in s:
        lists.append(v.to_dict())
    return jsonify(lists)


@app_views.route("/states/<id>", methods=["GET"])
def state_id(id):
    """id state retrieve json object"""
    date = storage.all('State').values()
    for x in date:
        if x.id == id:
            return jsonify(x.to_dict())
    abort(404)


@app_views.route("/states/<id>", methods=["DELETE"])
def state_delete(id):
    """delete state with id"""
    state = storage.get('State', id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def statePost():
    """Creates a new state"""
    date = request.get_json()
    if date is None:
        abort(400, "Not a JSON")
    if not date.get('name'):
        abort(400, "Missing name")
    nwe_date = State(**date)
    storage.new(nwe_date)
    storage.save()
    return jsonify(nwe_date.to_dict()), 201


@app_views.route('/states/<id>', methods=['PUT'])
def statePut(state_id=None):
    """Update a State object"""
    x = storage.get("State", state_id)
    if state_id and x:
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if data:
            for key, value in data.items():
                ignore = ["id", "state_id", "created_at", "updated_at"]
                if key != ignore:
                    setattr(x, key, value)
            x.save()
            return (jsonify(x.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
