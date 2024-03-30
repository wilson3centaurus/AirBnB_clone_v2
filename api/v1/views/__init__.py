#!/usr/bin/python3
from flask import Blueprint
from api.v1.views.index import *

# create a blueprint instance with url prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
