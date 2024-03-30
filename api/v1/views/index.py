#!/usr/bin/python3
"""index View"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieve the number of each object type"""
    counts = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(counts)
