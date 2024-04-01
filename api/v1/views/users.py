#!usr/bin/python3
""" Users View """

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users/', methods=["GET"], strict_slashes=False)
def users_get():
    """ gets users"""
    users = []
    for key, values in storage.all(User).items():
        users.append(values.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def get_user_with_id(user_id):
    """ gets user with id """
    users = storage.get(User, user_id)
    if not users:
        abort(404)

    return jsonify(users.to_dict())


@app_views.route('/users/<users_id>', methods=["DELETE"], strict_slashes=False)
def users_delete(user_id):
    """ deletes a user """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def user_post():
    """ creates a user """
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'email' not in data:
        abort(400, description="Missing email")

    if 'password' not in data:
        abort(400, description="Missing password")

    new_User = User(**data)
    new_User.save()
    return make_response(jsonify(new_User.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def users_put(user_id):
    """ updates a user """
    user = storage.get(User, user_id)
    data = request.get_json()

    if not user:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in to_ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
