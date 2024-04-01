#!/usr/bin/python3
"""
'Contains a Flask web application API.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

from api.v1.views import app_views
from models import storage


app = Flask(__name__)
'''The Flask web application instance.'''
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    The Flask app/request context end event listener.
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 error
    :return: returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return(resp)

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
