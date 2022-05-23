#!/usr/bin/python3
"""
Python flask
"""


from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def close(bruh):
    """Method that calls close storage"""
    storage.close()

@app.response_404
def error404(404):
    """ 404 handler """

    return {"error": "Not found"}


if __name__ == '__main__':
    app.run(
            host=getenv('HBNB_API_HOST') or '0.0.0.0',
            port=int(getenv('HBNB_API_PORT') or 5000),
            threaded=True
        )
