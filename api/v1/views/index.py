#!/usr/bin/python3
'''indexy boi'''
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def stat():
    return jsonify({'status':'OK'})
