#!/usr/bin/python3
"""
Module that handles:
    - Retrieval of list of all Review objects of a Place.
    - Retrieval of a Review object.
    - Deletion of a Review object.
    - Creation of a Review.
    - Updates a Review object.
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place


@app_view.route('/places/<place_id>/reviews',
                methods['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    Args:
        place_id: uuid of a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(city.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_a_review(review_id):
    """
    Retrieves a Review object.
    Args:
        review_id: uuid of a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review_response = review.to_dict()
    return (review_response)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_a_review(review_id):
    """
    Deletes a Review object
    Args:
         review_id: uuid of a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review_id)
    storage.save()
    return jsonify({}), 200


@app_view.route('/places/<place_id>/reviews',
                methods=['POST'], strict_slashes=False)
def create_a_review(place_id):
    """
    Creates a Review
    Args:
        place_id: uuid of a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")

    dataset = request.get_json()
    if 'user_id' not in dataset:
        abort(400, description="Missing user_id")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if 'text' not in dataset:
        abort(400, description="Missing text")

    review_response = review.to_dict()
    return jsonify(review_response, 200)


@app_view.route('/reviews/<review_id>',
                methods=['PUT'], strict_slashes=False)
def update_a_review(review_id):
    """
    Updates a reviw
    Args:
        review_id: uuid of a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")

    dataset = request.get_json()
    for k, v in dataset.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    review.save()

    review_response = review.to_dict()
    return jsonify(review_response), 200
