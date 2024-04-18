#!/usr/bin/python3
""" Flask Application 0.1 """

from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    # Main function
    host = environ.get('HBNB_API_HOST') or '0.0.0.0'
    port = environ.get('HBNB_API_PORT') or '5000'
    app.run(host=host, port=port, threaded=True)
