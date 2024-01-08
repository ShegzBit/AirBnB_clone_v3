#!/usr/bin/python3
""" State RESTful API definition
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """ Get the `Place` objetcs
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_from_id(place_id):
    """ Get a particular place with the given id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a place with the given id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create a new place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = request.get_json()
    if place is None:
        abort(400, 'Not a JSON')
    if 'name' not in place:
        abort(400, 'Missing name')

    new_place = Place(city_id=city_id, **place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a place with the given id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    new_place = request.get_json()
    if new_place is None:
        abort(400, 'Not a JSON')

    for key, value in new_place.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200
