#!/usr/bin/python3

import os
from flask import Flask
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def close_storage(exception):
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
