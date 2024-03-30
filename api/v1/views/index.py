#!/usr/bin/python3
""" api status """

from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def return_status():
    """ Return status """
    message = dict({
        "status": "OK"
        })
    return message
