#!/usr/bin/python3
"""Flask application"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

#flask app instance
app = Flask(__name__)

#blueprint registration
app.register_blueprint(app_views)


# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


#teardown method
@app.teardown_appcontext
def teardown_appcontext(exception):
    """close running SQLAlchemy session"""
    storage.close()


#handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    """a not found page"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
