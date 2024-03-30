#!/usr/bin/python3
""" Module to retrieve all state objects. """

from flask import Flask, abort, request, jsonify
from modules import storage
from models.state import State
from api.v1.views import app_views


app_views.url_map.strict_slashes=False


@app_views.route('/states', methods=['GET'])
def get_states():
    """ Function to handle the logic. """
    states = [state.to_dict() for state in storage.all('State').values()]

    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(s_id):
    """ Function toreturn state using the given id. """
    state = storage.get("State", s_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(s_id):
    """ Function to delete state obj using given state id. """
    state = storage.get("State", s_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Function to create a new state obj. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        obj_data = request.get_json()
        obj = State(**obj_data)
        obj.save()

        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<states_id>', methods=['PUT'])
def update_state(s_id):
    """ Function to update existing state object. """
    state_obj = storage.get("State", s_id)

    if state_obj is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj_data = request.get_json()
    state_obj.name = obj_data['name']
    state_obj.save()

    return jsonify(state_obj.to_dict()), 200
