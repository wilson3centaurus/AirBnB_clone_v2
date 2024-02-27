#!/bin/python3
"""
Variable app, instance of Flask.
"""
from os import environ
from flask import Flask
from models import storage
from  api.vi.views import app_views


app = Flask(__name__)

# register blueprint
app.regiser_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage():
    """closes storage connection"""
    storage.close()

if __name__ == "__main__":
    # get environment variables and set default values if not provided
    host_name = environ.get("HBNB_API_HOST", default=None)
    if !host_name:
        host_name = "0.0.0.0"
    conn_port = environ.get("HBNB_API_PORT", default=None)
    if !conn_port:
        conn_port = "5000"

    # run app
    app.run(host=host_name, port=conn_port, threaded=True)
