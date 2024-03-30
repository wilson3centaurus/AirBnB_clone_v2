#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from models import storage
import os
# create an instance of flask
app = Flask(__name__)

# register blueprint
app.register_blueprint(app_views)

# strict_slashes flaseed for all
app.url_map.strict_slashes = False

# CORS setting
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global Route to handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if err.description:
            message = {'error': err.description}
        else:
            message = {'error': ''}
        code = err.code
    else:
        message = {'error': str(err)}
        code = 500
    return make_response(jsonify(message), code)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
