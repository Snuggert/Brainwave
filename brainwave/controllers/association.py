"""association.py - Controller calls for association."""
from brainwave.models.association import Association
from brainwave.models.user import User
from brainwave.controllers.user import UserController
from brainwave import db


class AssociationController:
    """The Controller for association manipulation."""
    class NoNameGiven(Exception):
        """Exception for when no name is given for an association."""
        def __init__(self):
            self.error = 'No name was given for the association'

    class CustomerAlreadyCoupled(Exception):
        """Exception for when the association is already coupled to a
        customer."""
        def __init__(self):
            """Initialize with standard message."""
            self.error = 'The association is already coupled with the '\
                         'customer'

    class CustomerNotCoupled(Exception):
        """Exception for when the association is not coupled to a customer."""
        def __init__(self):
            """Initialize with standard message."""
            self.error = 'The association is not coupled with the customer.'

    @staticmethod
    def create(association_dict):
        """Create a new association."""
        association_dict['role'] = User.ROLE_ASSOCIATION
        user = UserController.create(association_dict)
        association_dict['user_id'] = user.id

        association = Association.new_dict(association_dict)

        if not association.name:
            raise AssociationController.NoNameGiven()

        db.session.add(association)
        db.session.commit()

        return association

    @staticmethod
    def update(association_dict):
        """Update the association."""
        association = Association.merge_dict(association_dict)

        if not association.name:
            raise AssociationController.NoNameGiven()

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

    @staticmethod
    def get_customers(association):
        """Get customers the association is coupled to."""
        return association.customers

    @staticmethod
    def customer_is_coupled(association, customer):
        """Check if the association is coupled to the customer."""
        try:
            association.customers.all().index(customer)
        except ValueError:
            return False

        return True

    @staticmethod
    def add_customer(association, customer):
        """Couple a customer to the association."""
        if AssociationController.customer_is_coupled(association, customer):
            raise AssociationController.CustomerAlreadyCoupled()

        association.customers.append(customer)
        db.session.add(association)
        db.session.commit()

    @staticmethod
    def remove_customer(association, customer):
        """Remove a customer the association is coupled to."""
        try:
            association.customers.remove(customer)
        except ValueError:
            raise AssociationController.CustomerNotCoupled()

        db.session.add(association)
        db.session.commit()
