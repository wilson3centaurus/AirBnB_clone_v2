#!/usr/bin/python3
"""
Main module for the API.
"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Teardown App Context.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''return render_template'''
    return jsonify('error='Not found'), 404


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
