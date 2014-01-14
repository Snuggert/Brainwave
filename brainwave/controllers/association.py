"""association.py - Controller calls for association."""
from brainwave.models.association import Association
from brainwave.models.user import ROLE_ASSOCIATION
from brainwave.controllers.user import UserController
from brainwave import db


class AssociationController:
    """The Controller for association manipulation."""
    @staticmethod
    def create(association_dict):
        """Create a new association."""

        association_dict['role'] = ROLE_ASSOCIATION
        user = UserController.create(association_dict)
        association_dict['user_id'] = user.id

        association = Association.new_dict(association_dict)
        db.session.add(association)
        db.session.commit()

        return association

    @staticmethod
    def delete(association):
        """Delete an association."""
        db.session.delete(association)
        db.session.commit()

    @staticmethod
    def get(association_id):
        """Get an association by its id."""
        return Association.query.get(association_id)

    @staticmethod
    def get_all():
        """Get all associations."""
        return Association.query.all()
