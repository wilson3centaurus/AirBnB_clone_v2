#!/usr/bin/python3
""" places view """

from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places',
                 methods=["GET"], strict_slashes=False)
def place_get(city_id):
    """ gets places"""
    city = storage.get(City, city_id)
    places = []
    if not city:
        abort(404)
    for place in city.places:
        places.append(city.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def get_place_with_id(place_id):
    """ gets place with id """
    places = storage.get(Place, place_id)
    if not places:
        abort(404)

    return jsonify(places.to_dict())


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def place_delete(place_id):
    """ deletes a place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=["POST"], strict_slashes=False)
def place_post(city_id):
    """ creates a place """
    city = storage.get(City, city_id)
    data = request.get_json()
    user = storage.get(User, data["user_id"])
    if not city:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, description="Missing name")

    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def place_put(place_id):
    """ updates a place """
    place = storage.get(Place, place_id)
    data = request.get_json()

    if not place:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']

    for key, value in data.items():
        if key not in to_ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

    
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """ search places """
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
