#!/usr/bin/python3
"""
Status of my API
"""
from os import getenv
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import jsonify
from flask_cors import CORS
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down_db(exception):
    """performing a cleanup task"""
    storage.close()

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)

@app.errorhandler(404)
def page_not_found(e):
    """handling not found templates"""
    error = {"error": "Not found"}
    return jsonify(error), 404


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
