#!/usr/bin/python
"""Start your API"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# save blueprint in app
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """Close storage"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
# app.run(host="HBNB_API_HOST", port="HBNB_API_PORT", threaded=True)
