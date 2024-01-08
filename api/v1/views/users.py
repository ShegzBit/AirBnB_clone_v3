#!/usr/bin/python3
""" State RESTful API definition
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Get the `User` objetcs
    """
    users = storage.all(User)
    return jsonify([user.to_dict() for obj in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users_from_id(user_id):
    """ Get a particular user with the given id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Delete a user with the given id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a new user
    """
    user = request.get_json()
    if user is None:
        abort(400, 'Not a JSON')
    if 'email' not in user:
        abort(400, 'Missing email')
    if 'password' not in user:
        abort(400, 'Missing password')

    new_user = User(**user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Update a user with the given id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    new_user = request.get_json()
    if new_user is None:
        abort(400, 'Not a JSON')

    for key, value in new_user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200
