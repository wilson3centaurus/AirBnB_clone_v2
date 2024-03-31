/usr/bin/python3
"""
Route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


# Retrieve all cities associated with a specific state
@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    Retrieves all City objects from a specific state.
    :param state_id: ID of the state
    :return: JSON of all cities in a state or 404 on error
    """
    city_list = []
    state_object = storage.get("State", state_id)

    if state_object is None:
        abort(404)
    for obj in state_object.cities:
        city_list.append(obj.to_json())

    return jsonify(city_list)


# Create a new city associated with a specific state
@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    Create a new city route.
    :param state_id: State ID
    :return: Newly created city object
    """
    create_json = request.get_json(silent=True)
    if create_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in create_json:
        abort(400, 'Missing name')

    create_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    response = jsonify(new_city.to_json())
    response.status_code = 201

    return response


# Retrieve a specific city by ID
@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_by_id(city_id):
    """
    Gets a specific City object by ID.
    :param city_id: City object ID
    :return: City object with the specified ID or error
    """
    retrived_obj = storage.get("City", str(city_id))

    if retrived_obj is None:
        abort(404)

    return jsonify(retrived_obj.to_json())


# Update a specific city by ID
@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    Updates a specific City object by ID.
    :param city_id: City object ID
    :return: City object and 200 on success, or 400 or 404 on failure
    """
    update_city = request.get_json(silent=True)
    if update_city is None:
        abort(400, 'Not a JSON')
    retrived_obj = storage.get("City", str(city_id))
    if retrived_obj is None:
        abort(404)
    for key, val in update_city.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(retrived_obj, key, val)
    retrived_obj.save()
    return jsonify(retrived_obj.to_json())


# Delete a specific city by ID
@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def city_delete_by_id(city_id):
    """
    Deletes a City by ID.
    :param city_id: City object ID
    :return: Empty dictionary with 200 or 404 if not found
    """
    delete_city = storage.get("City", str(city_id))

    if delete_city is None:
        abort(404)

    storage.delete(delete_city)
    storage.save()

    return jsonify({})
