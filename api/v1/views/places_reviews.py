#!/usr/bin/python3
"""
State view
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews_by_places(place_id=None):
    """Get all review objects"""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404)
    reviews = [review.to_dict() for review in place_by_id.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews(review_id=None):
    """Get review object based on ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/eviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes review object based on ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_reviews_by_places(place_id=None):
    """Creates new review object associated by Places"""
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if "user_id" not in req_json:
        abort(400, 'Missing user_id')
