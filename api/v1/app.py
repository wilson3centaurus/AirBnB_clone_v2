#!/usr/bin/python3
"""Create Flask app and register the blueprint app_views"""
from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """handling 404 error"""
    response = { "error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    """Main Function"""
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=HOST, port=PORT, threaded=True)
