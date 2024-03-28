#!/usr/bin/python3

import app_views from api.v1.views
import flask from Flask
import storage from models

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def end_session(exc):
    """ Ends the current session after each request """
    storage.close()


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
