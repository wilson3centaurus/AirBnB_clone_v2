#!/usr/bin/python3
'''Blueprint for /status'''


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], srtict_slahes=False)
def status():
    '''Returns JSON with status'''
    return jsonify({"status": "OK"})
