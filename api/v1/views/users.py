#!/usr/bin/python3
"""
    Users_view routes C.R.U.D methods
"""
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
        Retrieve all User objects.
        Returns:
            JSON: A JSON response containing dictionaries of the User objects.
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
        Retrieve a User object by ID.
        Args:
            user_id (str): The ID of the User.
        Returns:
            JSON: A JSON response containing the User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
        Delete a User object by ID.
        Args:
            user_id (str): The ID of the User.
        Returns:
            JSON: An empty JSON response with a status code of 200.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
        Create a User object.
        Returns:
            JSON: A JSON response containing the new User object.
    """
    if not request.json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
        Update a User object by ID.
        Args:
            user_id (str): The ID of the User.
        Returns:
            JSON: A JSON response containing the updated User object.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
