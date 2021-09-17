#!/usr/bin/python3
import os
from werkzeug.exceptions import NotFound
from flask import Flask, make_response, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(NotFound)
def handle_not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # runs the Flask application through port 5000 from local host
    app.run(host='0.0.0.0', port='5000', threaded=True)
