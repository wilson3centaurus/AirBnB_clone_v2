#!/usr/bin/python3
""" Flask Application 0.1 """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flask_restplus import Api

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title='Your API Title',
    description='Your API Description'
    )

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error """
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.errorhandler
def default_error_handler(e):
    """ Default Error Handler """
    return {'message': 'An unhandled exception occurred.'}, 500


if __name__ == "__main__":
    """ Main Function """

    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
