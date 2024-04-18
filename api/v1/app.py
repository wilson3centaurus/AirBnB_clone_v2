#!/usr/bin/python3
'''
    Entry point of the API

    This module creates the Flask app and registers the blueprint
'''
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flasgger import Swagger

# Create the Flask app
app = Flask(__name__)
app.register_blueprint(app_views)
swagger = Swagger(app)


@app.teardown_appcontext
def close_db(error):
    '''
        Function that closes the database
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''
        Error handler function that returns a
        JSON-formatted 404 status code response
    '''
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    '''
        Main function of the API
    '''
    # Get the host and port from the environment
    host = environ.get('HBNB_API_HOST') or '0.0.0.0'
    port = environ.get('HBNB_API_PORT') or '5000'

    app.run(host=host,
            port=port,
            threaded=True)
