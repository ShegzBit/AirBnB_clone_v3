#!/usr/bin/python3
""" State RESTful API definition
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ Get the `City` objetcs
    """
    states = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in states.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_from_id(city_id):
    """ Get a particular city with the given id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Delete a city with the given id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Create a new state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = request.get_json()
    if city is None:
        abort(400, 'Not a JSON')
    if 'name' not in city:
        abort(400, 'Missing name')

    new_city = City(state_id=state_id, **city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Update a city with the given id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    new_city = request.get_json()
    if new_city is None:
        abort(400, 'Not a JSON')

    for key, value in new_city.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200
