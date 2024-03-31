#!/usr/bin/python3
import storage from model
import flask from Flask
import app_views from api.v1.views

app = Flask(__name__)
app.blue_print(app_views, url_prefix='/api/v1')

@app.teardown_appcontext()

