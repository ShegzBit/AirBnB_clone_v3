#!/usr/bin/python3
"""
A new view for the link between Place objects and Amenity
objects that handles all default RESTFul API actions:
"""

from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, request
from models.place import Place
from models import storage, storage_t


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def amenities(place_id):
    """
    Get all amenities of place with given id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_t != 'db':
        amenities = [storage.get(Amentity, amn) for amn in place.amenity_ids]
    else:
        amenities = [amn for amn in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def unlink_amenity(place_id, amenity_id):
    """
    Deletes an amenity
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t != 'db':
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    else:
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    Link an Amenity with given id to a place with given id
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t != 'db':
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
    else:
        place.amenities.append(amenity)
    return jsonify(amenity.to_dict()), 201
