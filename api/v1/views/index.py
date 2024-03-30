#!/usr/bin/python3
"""
create Flask app, app_views
"""

from flask import jsonify, make_response, current_app
from api.v1.views import app_views
from models import storage

@app_views.route("/status")
def api_status():
    """returns status Ok if working"""
    response = make_response(jsonify({'status': "OK"}), 200)
    return (response)


@app._views.route("/stats")
def get_stats():
    """returns the stats of the api"""
    stats = {
            "amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storeage.count('Place'),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }

    return jsonify(stats)
