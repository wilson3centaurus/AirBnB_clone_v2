#!/usr/bin/python3
""" Init file """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
