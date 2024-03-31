#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}

@app_views.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=["GET"])
def stats():
    objs_count = {}

    for key, values in classes.items():
        objs_count[key] = storage.count(values)

    return jsonify(objs_count)
