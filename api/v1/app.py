#!/usr/bin/python3
"""
starts a Flask web application
"""

from api.v1.views import app_views
from flask import Flask
from models import storage

my_app = Flask(__name__)
my_app.register_blueprint(app_views)


@my_app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    my_app.run(host='0.0.0.0', port='5000', threaded=True)
