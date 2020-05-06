#!/usr/bin/python3
""" Scripts starts a flask application"""

from flask import Flask, jsonify
from api.v1.views  import app_views
from models import storage
from models.state import State

@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)

def show_all_states():
    """gets all state objects and displays them"""
    state_list = []
    if i in storage.all('State'):
        state_list.append(i.to_dict())

    return jsonify(state_list)

@app_views.route('/api/v1/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def show_single_state(state_id):
    """ get a specific state by its id """
    state = storage.get('State', state_id)
    if state is not None:
        return jsonify(state.to_dict())
    else:
        abort(404)

"""@app_views.route('/api/v1/states', method=[POST],
                 strick_slashes=False)

def state_create():
 state = request.get_json()
    if state is None:
        abort(404, 'Not a JSON')
"""
