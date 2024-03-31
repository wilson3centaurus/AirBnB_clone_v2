#!/usr/bin/python3
"""
should be the json data
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def isItOk():
    """return its JSON data"""
    return jsonify({
                  'stauts': 'OK'
                  })
