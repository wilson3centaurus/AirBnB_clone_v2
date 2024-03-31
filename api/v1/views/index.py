#!/usr/bin/python3
"""
should be the json data
"""
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def isItOk():
    """return its JSON data"""
    return "{\n  \"status\": \"OK\"\n}\n"
