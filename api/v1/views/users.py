#!/usr/bin/python3
"""
Module that handles:
    - Retrieval of list of all User objects of a State.
    - Retrieval of a User object.
    - Deletion of a User object.
    - Creation of a User.
    - Updates a User object
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all User objects """
    users = User.storage.all()
    users_json = []
    for user in users:
        user_json.append(user.to_dict())
    return jsonify(users_json), 200


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_a_user_using_id(user_id):
    """
    Retrieves a user object
    Parameters:
        user_id: uuid for user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_a_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/users',
                 methods=['POST'], strict_slashes=False)
def create_a_user():
    """ Creates a User """
    if not request.json:
        abort(400, description="Not a JSON")

    dataset = request.get_json()
    if 'email' not in request.json:
        abort(400, description="Missing email")
    if 'password' not in request.json:
        abort(400, description='Missing password')

    user = User(**dataset)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_a_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")

    dataset = request.get_json()
    for k, v in dataset.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()

    return jsonify(user.to_dict()), 200
