#!/usr/bin/python3
"""
creating a view for User objects
"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    '''RETRIEVE THE LIST OF ALL User OBJECTS'''
    obj_lst = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(obj_lst)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''retrive a user object by its id'''
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''delete a user object'''
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    '''create a user object'''
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    user_data = request.get_json()
    user = User(**user_data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    '''update a user by its id'''
    user = storage.get(User, user_id)
    data = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    if user:
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
    else:
        abort(404)
    storage.save()
    return jsonify(user.to_dict()), 200
