#!/usr/bin/python3
"""Contains a Flask web application API."""


import os
from flask import Flask
from flask import *
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_flask(exception):
    """App/request context end event listener."""
    storage.close()


if __name__ == '__main__':
    app.run(os.getenv("HBNB_API_HOST"), os.getenv("HBNB_API_PORT"))
