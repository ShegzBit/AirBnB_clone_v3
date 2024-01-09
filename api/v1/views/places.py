#!/usr/bin/python3
""" State RESTful API definition
"""
from flask import jsonify, abort, request
from functools import reduce

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


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
    if 'user_id' not in place:
        abort(400, 'Missing user_id')
    if storage.get(User, place['user_id']) is None:
        abort(404)
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
        if key not in (['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']):
            setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_place():
    """
    Searches for places based on given State and City
    and filters them based on amenity
    """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    cities = list(map(lambda id: storage.get(City, id), cities))
    states = list(map(lambda id: storage.get(State, id), states))
    for state in states:
        cities.extend(state.cities)
    main_cities = set()
    main_cities.update(cities)
    places = [city.places for city in main_cities]
    flat_places = []
    for place in places:
        flat_places.extend(place)
    flat_place_copy = flat_places[:]
    for place in flat_place_copy:
        if storage_t != 'db':
            if any(amn not in place.amenity_ids for amn in amenities):
                flat_places.remove(place)
        else:
            amenities = list(map(lambda id: storage.get(Amenity, id),
                                 amenities))
            if any(amn not in place.amenities for amn in amenities):
                flat_places.remove(place)
    if data == {}:
        flat_places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in flat_places])
