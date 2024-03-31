#!/usr/bin/python3
"""Creates Flask app"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """
    Returns a JSON with the status
    """
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each objects by type"""
    stats = {}
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]

    for cls_name in classes:
        cls_count = storage.count(cls_name)
        stats[cls_name] = cls_count

    return jsonify(stats)
