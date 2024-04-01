#!/usr/bin/python3
"""
Flask app: handle CORS, register blueprints, teardown, and error handling.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def teardown(exception):
    """
    Teardown function to close the SQLAlchemy session object after each request.
    """
    storage.close()

@app.errorhandler(404)
def handle_404(error):
    """
    Error handler for 404 Not Found errors.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404

if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
