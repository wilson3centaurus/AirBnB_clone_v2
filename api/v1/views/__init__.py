#!/usr/bin/python3
"""Blueprints intialization of APIs"""

from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


# wildcard importing of everything in the api.v1.views.index package
from api.v1.views.index import *
from api.v1.views.states import *
