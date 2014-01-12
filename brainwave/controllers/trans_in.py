"""trans_in.py - Controller for transaction-in."""
from flask import Blueprint, jsonify, request
from brainwave.api import TransInAPI
from brainwave.utils import serialize_sqla

trans_in_controller = Blueprint('trans_in_controller', __name__,
                                url_prefix='/api/trans_in')


@trans_in_controller.route('', methods=['POST'])
def create():
    """Create new trans_in item."""
    trans_in_dict = request.json

    trans_in = TransInAPI.create(trans_in_dict)

    return jsonify(id=trans_in.id)


@trans_in_controller.route('/<int:trans_in_id>', methods=['DELETE'])
def delete(trans_in_id):
    """Delete trans_in item."""
    trans_in = TransInAPI.get(trans_in_id)

    if not trans_in:
        return jsonify(error='Transaction-in item not found'), 500

    TransInAPI.delete(trans_in)

    return jsonify()


@trans_in_controller.route('/<int:trans_in_id>', methods=['GET'])
def get(trans_in_id):
    """Get trans_in item."""
    trans_in = TransInAPI.get(trans_in_id)

    if not trans_in:
        return jsonify(error='Transaction-in item not found'), 500

    return jsonify(trans_in=serialize_sqla(trans_in))
