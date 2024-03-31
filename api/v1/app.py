#!/usr/bin/python3
"""Flask Application"""
from models import storage
from flask import Flask
from api.v1.views import app_views
from os import environ

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """closes the storage"""
    storage.close()


if __name__ == "__main__":
    """Main Function"""
    host = environ.get("HBNB_API_HOST")
    port = environ.get("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
