#!/usr/bin/python3
""" A new view for place_amenity RESTful API definition
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """ Retrieves the list of all Amenity objects/ids of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_t == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    return jsonify([amenity for amenity in place.amenity_ids])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Deletes an Amenity object and links of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    if storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """ Link an Amenity with a given id to a place at a given id
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if storage_t != 'db':
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
        else:
            return jsonify(amenity.to_dict())
    else:
        if amenity not in place.amenities:
            place.amenities.append(amenity)
        else:
            return jsonify(amenity.to_dict())

    storage.save()
    return jsonify(amenity.to_dict()), 201
