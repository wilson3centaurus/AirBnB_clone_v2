#!/usr/bin/python3
"""API endpoints for User resources."""
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_all_users():
    """Returns a list of all User objects as JSON."""
    all_users = [u.to_dict() for u in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def fetch_user(user_id):
    """Fetches a User by their ID, returns JSON or 404 if not found."""
    user_instance = storage.get(User, user_id)
    if not user_instance:
        abort(404)
    return jsonify(user_instance.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def remove_user(user_id):
    """Removes a User by their ID, returns 200 JSON response on success."""
    user_to_delete = storage.get(User, user_id)
    if not user_to_delete:
        abort(404)
    user_to_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_new_user():
    """Creates a User from JSON request data, returns JSON response."""
    user_data = request.get_json()
    if not user_data:
        abort(400, description="Not a JSON")
    required_fields = ['email', 'password']
    if any(field not in user_data for field in required_fields):
        abort(400, description=f"Missing {', '.join(required_fields)}")
    new_user = User(**user_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def modify_user(user_id):
    """Updates a User's attributes except for id, email, created_at, and updated_at."""
    user_to_modify = storage.get(User, user_id)
    if not user_to_modify:
        abort(404)
    update_data = request.get_json()
    if not update_data:
        abort(400, description="Not a JSON")
    for key, value in update_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_to_modify, key, value)
    user_to_modify.save()
    return jsonify(user_to_modify.to_dict())
