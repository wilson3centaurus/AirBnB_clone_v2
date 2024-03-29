#!/usr/bin/python3
"""
starts a Flask web application
"""
from api.v1.views import app_views
from flask import Flask
from models import storage
import os
# create an instance of flask
app = Flask(__name__)

# register blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
