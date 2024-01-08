#!usr/bin/python3
""" State RESTful API definition
"""
from flask import jsonify, abort, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Get the `State` objetcs
    """
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_from_id(state_id):
    """ Get a particular state with the given id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Delete a state with the given id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create a new state
    """
    state = request.get_json()
    if state is None:
        abort(400, 'Not a JSON')
    if 'name' not in state:
        abort(400, 'Missing name')

    new_state = State(**state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update a state with the given id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    new_state = request.get_json()
    if new_state is None:
        abort(400, 'Not a JSON')

    for key, value in new_state.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
