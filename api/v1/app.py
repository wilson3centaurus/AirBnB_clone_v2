#!/usr/bin/python3
"""Contains a Flask web application API."""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register the blueprint app_views to flask instance app
app.register_blueprint(app_views)


# Declare a method to handle @pp.teardown_appcontext that calls storage.close function
@app.teardown_appcontext
def close_storage(exception):
    storage.close()


# Run Flask Server
if __name__ == "__main__":
    # Define host and port base on environment variables
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    # Run Flask application
    app.run(host=host, port=port, threaded=True)
