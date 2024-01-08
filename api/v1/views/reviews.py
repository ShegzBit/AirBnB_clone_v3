#!/usr/bin/python3
""" Place_review RESTful API definition
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_of_place_id(place_id):
    """ Get the `Review` objetcs with a `place_id`
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews_from_id(review_id):
    """ Get a particular review with the given id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a review with the given id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create a new review of a place
    """
    if storage.get(Place, place_id) is None:
        abort(404)

    new_review = request.get_json()
    if new_review is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in new_review:
        abort(400, 'Missing user_id')
    if storage.get(User, new_review['user_id']) is None:
        abort(404)

    if 'text' not in new_review:
        abort(400, 'Missing text')

    new_review['place_id'] = place_id
    review = Review(**new_review)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update a review with the given id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    new_review = request.get_json()
    if new_review is None:
        abort(400, 'Not a JSON')

    for key, value in new_review.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()

    return jsonify(review.to_dict()), 200
