#!/usr/bin/python3

from flask import jsonify
from api.v1.views import app_views
from models import storage


# Define a route /status on the object app_views
@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """Retrieve stats of objects by type"""
    counts = {}
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']

    for cls_name in classes:
        cls = getattr(storage, cls_name)
        count = storage.count(cls)
        counts[cls_name] = count

    return jsonify(counts)
