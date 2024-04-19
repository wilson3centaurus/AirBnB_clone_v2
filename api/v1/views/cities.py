#!/usr/bin/python3
'''
    City module for the API
'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


# Route that returns a JSON response with all City objects
@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    '''
        Get all City objects by State ID
    '''
    state = storage.get(State, state_id)

    # If the state object was not found
    if not state:
        abort(404)

    # Create a list of all City objects in the State
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())

    # Return a JSON response with all City objects
    return jsonify(cities_list)


# Route that returns a JSON response with all City objects
@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''
        Get a City object by ID
    '''
    city = storage.get(City, city_id)

    # If the city object was found
    if city is None:
        abort(404)

    # Return the City object with a status of 200
    return jsonify(city.to_dict())


# Route that deletes a City object by ID
@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''
        Delete a City object by ID
    '''
    city = storage.get(City, city_id)

    # If the city object was not found
    if city is None:
        abort(404)

    # Delete the City object
    storage.delete(city)
    storage.save()

    # Return an empty dictionary with a status of 200
    return jsonify({}), 200


# Route that creates a City object
@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''
        Create a new City object
    '''
    state = storage.get(State, state_id)

    # If the state object was not found
    if state is None:
        abort(404)

    # If the request is not in JSON format
    if not request.json:
        abort(400, 'Not a JSON')

    # If the request does not contain the key 'name'
    if 'name' not in request.json:
        abort(400, 'Missing name')

    # Get the JSON request
    data = request.json
    data['state_id'] = state_id
    new_city = City(**data)

    # Save the new City object
    storage.new(new_city)
    storage.save()

    # Return the new City object with a status of 201
    return jsonify(new_city.to_dict()), 201


# Route that updates a City object by ID
@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
        Update a City object by ID
    '''
    city = storage.get(City, city_id)

    # If the city object was not found
    if city is None:
        abort(404)

    # If the request is not in JSON format
    if not request.json:
        abort(400, 'Not a JSON')

    # Get the JSON request
    data = request.json
    # Update the City object with the JSON request data
    for key, value in data.items():
        if key not in ('id', 'state_id',
                       'created_at', 'updated_at'):
            # Set the attribute
            setattr(city, key, value)

    # Save the City object
    storage.save()

    # Return the City object with a status of 200
    return jsonify(city.to_dict()), 200
