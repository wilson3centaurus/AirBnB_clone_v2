#!/usr/bin/python3
""" This module handles the users routes
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


def get_object_by_id(cls, obj_id):
    """ This function is used to retrive a specific object using its id
    """
    for _, obj in storage.all(cls).items():
        if obj.id == obj_id:
            return obj
    return None


@app_views.route(
        "/users",
        methods=['GET'],
        strict_slashes=False)
def retrive_all_users():
    """ This function return list of all users """
    return [obj.to_dict() for _, obj in storage.all(User).items()]


@app_views.route(
        "/users/<user_id>",
        methods=['GET'],
        strict_slashes=False)
def retrive_user(user_id):
    """ This function is used to retrive a specific user
        object using its id
    """
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
        "/users/<user_id>",
        methods=['DELETE'],
        strict_slashes=False)
def delete_user(user_id):
    """ This function is used to delete an user object when
        the DELETE method is called
    """
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/users",
        methods=['POST'],
        strict_slashes=False)
def create_user():
    """ This function creates a new user object
    """
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Not a JSON")
    if "email" not in request_data:
        abort(400, "Missing email")
    if "password" not in request_data:
        abort(400, "Missing password")

    new_user = User(**request_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route(
        "/users/<user_id>",
        methods=['PUT'],
        strict_slashes=False)
def update_user(user_id):
    """ This function updates an existing user object
    """
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Not a JSON")

    for key, value in request_data.items():
        if key not in ('id, email, created_at, updated_at'):
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
