#!/usr/bin/python3
""" The module to handle view of the RESTful API for class User. """
from flask import Flask, abort, request, jsonify
from models import storage
from models.user import User
from api.v1.views import app_views


app_views.url_map.strict_slashes = False


@app_views.route('/users', methods=['GET'])
def get_users():
    """ Function to retrieve the list of all User objects. """
    users = [u.to_dict() for u in storage.all('User').values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_id(u_id):
    """ Function that retrieves a User object using GET. """
    user = storage.get("User", u_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(u_id):
    """ Function that deletes a User object. """
    user = storage.get("User", u_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """ Function that creates a User. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    elif "password" not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    else:
        obj_data = request.get_json()
        user_obj = User(**obj_data)
        user_obj.save()
        return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(u_id):
    """ FUnction that updates a User object. """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    obj_data = request.get_json()
    ignore = ("id", "email", "created_at", "updated_at")
    for key in obj_data.keys():
        if key in ignore:
            pass
        else:
            setattr(User_obj, key, obj_data[key])
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
