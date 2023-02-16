#!/usr/bin/python3

"""Bootstap for api"""

from api.v1.views import app_views
from models import storage
from os import getenv
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={r"/*": {"origin": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """if route does not exist"""
    return {"error": "Not found"}


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST", "0.0.0.0"), getenv(
        "HBNB_API_PORT", 5000), threaded=True)
