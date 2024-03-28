#!/usr/bin/python3
"""init file for views directory
creating the blueprint"""
from flask import Blueprint


app_views = Blueprint('first_blueprint',
                      __name__, url_prefix='/api/v1')
from api.v1.views.index import *
