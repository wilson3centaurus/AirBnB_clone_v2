#!/usr/bin/python3
"""API index view"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def attain_status():
    """Attain API status"""
    return jsonify(status='OK')
