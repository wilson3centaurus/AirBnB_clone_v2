#!/usr/bin/python3
"""application entry point"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def handle_application(application):
    """handle application"""
    storage.close()


@app.route('/api/v1/notexist')
def not_exist():
    """Handle 404 not found error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """entry point"""
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
