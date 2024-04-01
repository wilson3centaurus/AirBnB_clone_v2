#!usr/bin/python3
""" Reviews View """

from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews',
                 methods=["GET"], strict_slashes=False)
def reviews_get(place_id):
    """ gets users"""
    reviews = []
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    for review in place.reviews:
        reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def get_review_with_id(review_id):
    """ gets user with id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=["DELETE"], strict_slashes=False)
def reviews_delete(review_id):
    """ deletes a review """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=["POST"], strict_slashes=False)
def review_post(place_id):
    """ creates a review """
    place = storage.get(Place, place_id)
    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not place:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, description="Missing text")

    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def reviews_put(review_id):
    """ updates a review """
    review = storage.get(Review, review_id)
    data = request.get_json()

    if not review:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    to_ignore = ['id', 'user_id', 'created_at', 'updated_at', 'place_id']

    for key, value in data.items():
        if key not in to_ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
