#!/usr/bin/python3

"""
implement status route
return the status of API
"""


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)




@app.teardown_appcontext
def teardown(self):
    """
    close storage session
    """
    storage.close()


if __nam== "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"), port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
