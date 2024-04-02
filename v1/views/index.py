#!/usr/bin/python3

"""
create a route /status on the object app_views
returns a JSON "status": "OK"
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
    returns status
    """
    return jsonify({'status': 'OK'})
