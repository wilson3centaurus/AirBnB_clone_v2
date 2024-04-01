i#!/usr/bin/python3
"""API endpoints for places"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    to_be_ignored = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in to_be_ignored:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """API for places search"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places_coll = []
    if not (states and cities and amenities):
        places_coll = storage.all(Place).values()

    else:
        states_coll = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                states_coll.append(state)

        cities_coll = []
        for state in states_coll:
            for city in state.cities:
                cities_coll.append(city)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                cities_coll.append(city)

        cities_coll = list(set(cities_coll))

        places_coll = []
        for city in cities_coll:
            for place in city.places:
                places_coll.append(place)

    amenities_coll = []
    for amenity_id in amenities:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            amenities_coll.append(amenity)
    places_coll = list(set(places_coll))

    final_result = []
    for place in places_coll:
        place_dict = place.to_dict()
        if amenities_coll:
            if all(amenity in place.amenities for amenity in amenities_coll):
                final_result.append(place_dict)
        else:
            final_result.append(place_dict)

    return jsonify(final_result)i#!/usr/bin/python3
"""API endpoints for places"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    to_be_ignored = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in to_be_ignored:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """API for places search"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places_coll = []
    if not (states and cities and amenities):
        places_coll = storage.all(Place).values()

    else:
        states_coll = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                states_coll.append(state)

        cities_coll = []
        for state in states_coll:
            for city in state.cities:
                cities_coll.append(city)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                cities_coll.append(city)

        cities_coll = list(set(cities_coll))

        places_coll = []
        for city in cities_coll:
            for place in city.places:
                places_coll.append(place)

    amenities_coll = []
    for amenity_id in amenities:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            amenities_coll.append(amenity)
    places_coll = list(set(places_coll))

    final_result = []
    for place in places_coll:
        place_dict = place.to_dict()
        if amenities_coll:
            if all(amenity in place.amenities for amenity in amenities_coll):
                final_result.append(place_dict)
        else:
            final_result.append(place_dict)

    return jsonify(final_result)
