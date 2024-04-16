#!/usr/bin/python3
"""
This module provides flask app routing certain view pages.
"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)



@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the storage."""
    storage.close()


if __name__ == "__main__":
    app.register_blueprint(app_views, url_prefix="/api/v1")
    app.run(host='0.0.0.0', port=5000, threaded=False)
