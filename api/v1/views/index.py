#!/usr/bin/python3
""" This script shall start a Flask web application """
from app import app
from flask import jsonify
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from models.state import State
from os import getenv


@app.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ This instance shall return a JSON-formatted status response """
    return jsonify({"status": "OK"})
