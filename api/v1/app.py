#!/usr/bin/python3
'''Flask server app var'''

from models import storage
from api.v1.views import app_views
from flask import Flask


# Create a variable app, instance from flask
app = Flask(__name__)

# register the blueprint app_views to your app
app.register_blueprint(app_views)

# disables this strict trailing slash behavior.
app.url_map.strict_slashes = False

# method to handle the close of the app
@app.teardown_appcontext
def donw_method():
	""" close the storage"""
    storage.close()


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
