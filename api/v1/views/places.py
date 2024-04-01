#!/usr/bin/python3
"""
handles all RESTful API action for places
"""
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import request, abort, jsonify
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def places(city_id):
    """handles creating and retrieving of places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "POST":
        request_data = request.get_json()
        if request_data:
            if "user_id" not in request_data:
                abort(400, "Missing user_id")
            if "name" not in request_data:
                abort(400, "Missing name")
            user_id = request_data["user_id"]
            user = storage.get(User, user_id)
            if not user:
                abort(404)
            request_data["city_id"] = city_id
            place = Place(**request_data)
            place.save()
            return place.to_dict(), 201
        abort(400, "Not a JSON")
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())
    return places_list, 200


@app_views.route('/places/<place_id>',
                strict_slashes=False,
                methods=['GET', 'PUT', 'DELETE']
               )
def retrieve_update_delete_place(place_id):
    """retrieves delete and update a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "PUT":
        request_data = request.get_json()
        if request_data:
            for key, value in request_data.items():
                if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
                    setattr(place, key, value)
            place.save()
            return place.to_dict(), 200
        abort(400, "Not a JSON")
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return {}, 200
    return place.to_dict(), 200

