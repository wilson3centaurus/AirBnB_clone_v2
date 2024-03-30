#!/usr/bin/python3
"""Creates flask app"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def api_status():
    """
    returns a JSON
    """
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route('/stats')
def get_stats():
    """
    """
    stats = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'users': storage.count('User'),
            'places': storage.count('Place'),
            'states': storage.count('State'),
            'users': storage.count('User'),
            }
    return jsonify(stats)
