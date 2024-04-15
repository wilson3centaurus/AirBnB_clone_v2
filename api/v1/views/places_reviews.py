#!/usr/bin/python3
"""API endpoints for Review management."""
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def fetch_reviews(place_id):
    """Returns all Review objects associated with a given Place."""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    review_list = [review.to_dict() for review in place_obj.reviews]
    return jsonify(review_list)


@app_views.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def fetch_review(review_id):
    """Retrieves a specific Review by ID."""
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def erase_review(review_id):
    """Deletes a Review based on its ID."""
    review_to_remove = storage.get(Review, review_id)
    if not review_to_remove:
        abort(404)
    review_to_remove.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'], strict_slashes=False)
def add_review(place_id):
    """Creates a Review for a specific Place based on JSON input."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in review_data:
        abort(400, description="Missing user_id")
    user_obj = storage.get(User, review_data['user_id'])
    if not user_obj:
        abort(404)
    if 'text' not in review_data:
        abort(400, description="Missing text")
    new_review = Review(place_id=place_id, **review_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def edit_review(review_id):
    """Updates an existing Review object with new JSON data."""
    existing_review = storage.get(Review, review_id)
    if not existing_review:
        abort(404)
    updated_data = request.get_json()
    if not updated_data:
        abort(400, description="Not a JSON")
    for key, value in updated_data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(existing_review, key, value)
    existing_review.save()
    return jsonify(existing_review.to_dict())
