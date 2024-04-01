#!/usr/bin/python3
"""handles amenities request"""
from flask import abort, jsonify, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def users():
    """handles getting all amenities and creating amenities"""
    if request.method == "POST":
        request_data = request.get_json()
        if request_data:
            if "email" not in request_data:
                abort(400, "Missing email")
            if "password" not in request_data:
                abort(400, "Missing password")
            user = User(**request_data)
            user.save()
            return user.to_dict(), 201

        abort(400, "Not a JSON")
    all_users = []
    for user in storage.get_all(User):
        all_users.append(user.to_dict())
    return all_users


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def retrieve_delete_update_users(user_id):
    """retrieve, delete and update and user based on id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == "PUT":
        request_data = request.get_json()
        if request_data:
            for key, value in request_data.items():
                if key not in ["id", "email", "updated_at", "created_at"]:
                    setattr(user, key, value)
            user.save()
            return user.to_dict(), 200
    if request.method == "DELETE":
        user.delete()
        storage.save()
        return {}, 200
    return user.to_dict(), 200
