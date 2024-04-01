#!/usr/bin/python3

from . import index
from flask import Blueprint

from api.v1.views.index import app_views


# Create a Blueprint instance with URL prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
