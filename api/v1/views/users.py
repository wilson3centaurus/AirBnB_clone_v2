#!/usr/bin/python3
"""
    This is the users page handler for Flask.
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    return jsonify([user.to_dict() for user in storage.all(User).values()])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, 'Missing email' if not data else 'Not a JSON')
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at', 'password']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
