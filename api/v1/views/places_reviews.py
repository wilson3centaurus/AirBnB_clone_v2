#!/usr/bin/python3
""" Place Reviews Module """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get(place_id):
    """ Returns a list of Reviews objects """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        all_reviews = storage.all(Review)
        reviews = []
        for obj in all_reviews.values():
            if obj.place_id == place_id:
                reviews.append(obj.to_dict())
        return make_response(jsonify(reviews), 200)
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def one_review(review_id):
    """ Returns one review object """
    obj = storage.get(Review, review_id)
    if obj:
        return make_response(jsonify(obj.to_dict()), 200)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review obj if it exists """
    obj = storage.get(Review, review_id)
    if obj:
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createReview(place_id):
    """ Creates a new Review object using a place_id """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        if request.is_json is True:
            data = request.get_json()
        abort(400)
