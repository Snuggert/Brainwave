"""association.py - Controller calls for association."""
from brainwave.models.association import Association
from brainwave import db


class AssociationController:
    """The Controller for association manipulation."""
    @staticmethod
    def create(association_dict):
        """Create a new association."""
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
