#!/usr/bin/python3
""" states views """
from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route(
        '/states',
        methods=['GET'],
        strict_slashes=False)
def retrieve_states():
    """ retrieve all existing states """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route(
        '/states/<state_id>',
        methods=['GET'],
        strict_slashes=False)
def retrieve_state(state_id):
    """ to retrieve a needed state from states table"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_state(state_id):
    """ delete existing state and save """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route(
        '/states',
        methods=['POST'],
        strict_slashes=False)
def create_state():
    """create a state using POST methos """
    if not request.json:
        abort(400, "NOT a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    state_info = request.get_json()
    n_state = State(**state_info)
    n_state.save()
    return jsonify(n_state.to_dict()), 201


@app_views.route(
        '/states/<state_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_state(state_id):
    """ update state put method """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "NOT a JSON")
    state_info = request.get_json()
    for k, v in state_info.items():
        to_ignore = ['id', 'updated_at', 'created_at']
        if k not in to_ignore:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
