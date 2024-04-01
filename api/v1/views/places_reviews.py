#!/usr/bin/python3
from flask import abort, jsonify, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage

from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                    strict_slashes=False,
                    methods=['GET', 'POST'])
def reviews(place_id):
    """handles creating and retrieving of reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "POST":
        request_data = request.get_json()
        if request_data:
            if "user_id" not in request_data:
                abort(400, "Missing user_id")
            if "text" not in request_data:
                abort(400, "Missing text")
            user_id = request_data["user_id"]
            user = storage.get(User, user_id)
            if not user:
                abort(404)
            request_data["place_id"] = place_id
            review = Review(**request_data)
            review.save()
            return review.to_dict(), 201
        abort(400, "Not a JSON")
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return reviews, 200


@app_views.route('/reviews/<review_id>',
                    strict_slashes=False,
                    methods=['GET', 'PUT', 'DELETE'])
def retrieve_update_delete_review(review_id):
    """retrieves delete and update a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == "PUT":
        request_data = request.get_json()
        if request_data:
            for key, value in request_data.items():
                if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
                    setattr(review, key, value)
            review.save()
            return review.to_dict(), 200
        abort(400, "Not a JSON")
    if request.method == "DELETE":
        review.delete()
        storage.save()
        return {}, 200
    return review.to_dict(), 200

