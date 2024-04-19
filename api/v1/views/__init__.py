#!/usr/bin/python3
'''
    Initialize the blueprints for the API
'''
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import all view modules here
from api.v1.views.index import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.reviews import *
from api.v1.views.users import *
from api.v1.views.states import *
