#!/usr/bin/python3
"""
Route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity

# Retrieve all amenities
@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    Retrieves all Amenity objects.
    :return: JSON of all amenities
    """
    amenity_list = []
    amenity_objects = storage.all("Amenity")
    for obj in amenity_objects.values():
        amenity_list.append(obj.to_json())

    return jsonify(amenity_list)

# Create a new amenity
@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    Create amenity route.
    :return: Newly created amenity object
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    response = jsonify(new_amenity.to_json())
    response.status_code = 201

    return response

# Retrieve a specific amenity by ID
@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Gets a specific Amenity object by ID.
    :param amenity_id: Amenity object ID
    :return: Amenity object with the specified ID or error
    """

    retrived_obj = storage.get("Amenity", str(amenity_id))

    if retrived_obj is None:
        abort(404)

    return jsonify(retrived_obj.to_json())

# Update a specific amenity by ID
@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    Updates specific Amenity object by ID.
    :param amenity_id: Amenity object ID
    :return: Amenity object and 200 on success, or 400 or 404 on failure
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    retrived_obj = storage.get("Amenity", str(amenity_id))
    if retrived_obj is None:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(retrived_obj, key, val)
    retrived_obj.save()
    return jsonify(retrived_obj.to_json())

# Delete a specific amenity by ID
@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    Deletes Amenity by ID.
    :param amenity_id: Amenity object ID
    :return: Empty dictionary with 200 or 404 if not found
    """

    retrived_obj = storage.get("Amenity", str(amenity_id))

    if retrived_obj is None:
        abort(404)

    storage.delete(retrived_obj)
    storage.save()

    return jsonify({})
