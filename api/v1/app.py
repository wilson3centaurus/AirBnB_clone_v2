#!/usr/bin/python3
""" Starting Flask Application """


from flask import Flask, jsonify
from models import storage
from api.vi.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardwon_appcontext
def teardown(self):
    """ Call storage.close """
    storage.close()



if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True )
