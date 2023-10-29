#!/usr/bin/python3

from flask import Blueprint


app_views = Blueprint('app_views', __name__)

# This wildcard import is used to include views from other files.
# PEP8 may complain about it, but it's normal and can be ignored.
from api.v1.views.index import *
