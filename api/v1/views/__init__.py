#!/usr/bin/python3
'''
    Initialize the blueprints for the API
'''
from api.v1.views.index import *
from flask import Blueprint


# Create the blueprint object
app_views = Blueprint('app_views', __name__,
                      url_prefix='/api/v1')
