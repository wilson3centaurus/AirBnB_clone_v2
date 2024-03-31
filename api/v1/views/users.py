#!/usr/bin/python3
"""
Route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User

# Retrieve all users
@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    Retrieves all User objects.
    :return: JSON of all users
    """
    user_list = []
    user_objects = storage.all("User")
    for obj in user_objects.values():
        user_list.append(obj.to_json())

    return jsonify(user_list)

# Create a new user
@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    Create user route.
    :return: Newly created user object
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    response = jsonify(new_user.to_json())
    response.status_code = 201

    return response

# Retrieve a specific user by ID
@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    Gets a specific User object by ID.
    :param user_id: User object ID
    :return: User object with the specified ID or error
    """

    retrived_obj = storage.get("User", str(user_id))

    if retrived_obj is None:
        abort(404)

    return jsonify(retrived_obj.to_json())

# Update a specific user by ID
@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    Updates specific User object by ID.
    :param user_id: User object ID
    :return: User object and 200 on success, or 400 or 404 on failure
    """
    user_json = request.get_json(silent=True)

    if user_json is None:
        abort(400, 'Not a JSON')

    retrived_obj = storage.get("User", str(user_id))

    if retrived_obj is None:
        abort(404)

    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(retrived_obj, key, val)

    retrived_obj.save()

    return jsonify(retrived_obj.to_json())

# Delete a specific user by ID
@app_views.route("/users/<user_id>",  methods=["DELETE"],
                 strict_slashes=False)
def user_delete_by_id(user_id):
    """
    Deletes User by ID.
    :param user_id: User object ID
    :return: Empty dictionary with 200 or 404 if not found
    """

    retrived_obj = storage.get("User", str(user_id))

    if retrived_obj is None:
        abort(404)

    storage.delete(retrived_obj)
    storage.save()

    return jsonify({})
