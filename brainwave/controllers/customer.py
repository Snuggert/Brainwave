"""customer.py - Controller calls for customer."""
from werkzeug.security import generate_password_hash
from brainwave.models import Customer, Credit, User, Association
from brainwave import db
from brainwave.controllers import AssociationController
from flask import session


class CustomerController:
    """The Controller for customer manipulation."""
    class NoNameGiven(Exception):
        """Exception for when no name is given for a customer."""
        def __init__(self):
            self.error = 'No name was given for the customer'

    class AssociationAlreadyCoupled(Exception):
        """Exception for when the customer is already coupled to an
        association."""
        def __init__(self):
            """Initialize with standard message."""
            self.error = 'The customer is already coupled with the '\
                         'association'

    class AssociationNotCoupled(Exception):
        """Exception for when the customer is not coupled to an assocation."""
        def __init__(self):
            """Initialize with standard message."""
            self.error = 'The customer is not coupled with the assocation'

    @staticmethod
    def create(customer_dict):
        """Create a new customer."""
        if not 'username' in customer_dict:
            customer_dict['username'] = customer_dict['name']

        customer = Customer.new_dict(customer_dict)
        if not customer.name:
            raise CustomerController.NoNameGiven()

        db.session.add(customer)
        db.session.commit()

        return customer

    @staticmethod
    def update(customer_dict):
        """Update a customer."""
        customer = Customer.merge_dict(customer_dict)

        if not customer.name:
            raise CustomerController.NoNameGiven()

        db.session.add(customer)
        db.session.commit()

        return customer

    @staticmethod
    def delete(customer):
        """Delete a customer."""
        db.session.delete(customer)
        db.session.commit()

    @staticmethod
    def get(customer_id):
        """Get a customer by its id."""
        return Customer.query.get(customer_id)

    @staticmethod
    def get_all():
        """Get all customers."""
        if session['user_role'] >= User.ROLE_ADMIN:
            return Customer.query.all()
        if session['user_role'] >= User.ROLE_ASSOCIATION:
            ass = AssociationController.get(session['association_id'])
            return Customer.query. \
                filter(Customer.associations.contains(ass)).all()

    @staticmethod
    def get_all_all():
        """Hack method for Mats, by Jaap"""
        return Customer.query.all()

    @staticmethod
    def get_associations(customer):
        """Get associations the customer is coupled to."""
        return customer.associations

    @staticmethod
    def association_is_coupled(customer, association):
        """Check if the customer is coupled to the association."""
        try:
            customer.associations.all().index(association)
        except ValueError:
            return False

        return True

    @staticmethod
    def add_association(customer, association):
        """Couple an association to the customer."""
        # Check if the customer is already coupled to the association.
        if CustomerController.association_is_coupled(customer, association):
            raise CustomerController.AssociationAlreadyCoupled()

        customer.associations.append(association)
        db.session.add(customer)
        db.session.commit()

        # Create credit.
        credit = Credit(0.0, customer, association)
        db.session.add(credit)
        db.session.commit()

        customer.credits.append(credit)
        db.session.add(customer)
        db.session.commit()

    @staticmethod
    def remove_association(customer, association):
        """Remove an association the customer is coupled to."""
        # Remove credit.
        credit = customer.credits\
            .filter(Credit.association_id == association.id).first()
        db.session.delete(credit)
        db.session.commit()

        try:
            customer.associations.remove(association)
        except ValueError:
            raise CustomerController.AssociationNotCoupled()

        db.session.add(customer)
        db.session.commit()
