"""association.py - Controller for association."""
from flask import Blueprint, jsonify, request
from brainwave.controllers.association import AssociationController
from brainwave.utils import serialize_sqla

association_api = Blueprint('association_api', __name__,
                            url_prefix='/api/association')


@association_api.route('', methods=['POST'])
def create():
    """Create a new association."""
    association_dict = request.json

    try:
        association = AssociationController.create(association_dict)
    except AssociationController.NoPassword as e:
        return jsonify(error=e.error), 500

    return jsonify(id=association.id, pw_hash=association.pw_hash)


@association_api.route('/<int:association_id>', methods=['PUT'])
def update(association_id):
    """Update an association."""
    association_dict = request.json

    association = AssociationController.update(association_dict)

    return jsonify(pw_hash=association.pw_hash)


@association_api.route('/<int:association_id>', methods=['DELETE'])
def delete(association_id):
    """Delete an association."""
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    AssociationController.delete(association)

    return jsonify()


@association_api.route('/<int:association_id>', methods=['GET'])
def get(association_id):
    """Get an association."""
    association = AssociationController.get(association_id)

    if not association:
        return jsonify(error='Association not found'), 500

    return jsonify(association=serialize_sqla(association))
