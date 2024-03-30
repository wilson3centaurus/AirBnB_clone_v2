#!/usr/bin/python3
"""Creating a Flask app"""

from api.v1.views import app_views
from flask import jsonify

# Defines route /status
@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

