"""association.py - Controller for association."""
from flask import Blueprint, jsonify, request
from brainwave.api.association import AssociationAPI
from brainwave.utils import serialize_sqla

association_controller = Blueprint('association_controller', __name__,
                                   url_prefix='/api/association')


@association_controller.route('', methods=['POST'])
def create():
    """Create a new association."""
    association_dict = request.json

    try:
        association = AssociationAPI.create(association_dict)
    except AssociationAPI.NoPassword as e:
        return jsonify(error=e.error), 500

    return jsonify(id=association.id, pw_hash=association.pw_hash)


@association_controller.route('/<int:association_id>', methods=['PUT'])
def update(association_id):
    """Update an association."""
    association_dict = request.json

    association = AssociationAPI.update(association_dict)

    return jsonify(pw_hash=association.pw_hash)


@association_controller.route('/<int:association_id>', methods=['DELETE'])
def delete(association_id):
    """Delete an association."""
    association = AssociationAPI.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    AssociationAPI.delete(association)

    return jsonify()


@association_controller.route('/<int:association_id>', methods=['GET'])
def get(association_id):
    """Get a association."""
    association = AssociationAPI.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    return jsonify(association=serialize_sqla(association))
