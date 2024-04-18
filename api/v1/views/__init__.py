#!/usr/bin/python3
"""Define a Blueprint for API routes v1"""
from flask import Blueprint
from api.v1.views.index import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
