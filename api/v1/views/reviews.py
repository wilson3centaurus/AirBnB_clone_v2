#!/usr/bin/python3
'''
Reviews view for the API
'''

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.review import Review
from models import storage

@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    reviews = [
        review.to_dict() for review in storage.all(Review).values()]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ Deletes a specific Review object by ID """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route('/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review():
    """ Creates a new Review object """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Bad request: JSON data with "name" field is required')
    new_review = Review(name=data['name'])
    new_review.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates an existing Review object by ID """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, 'Bad request: JSON data is required for updating')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
