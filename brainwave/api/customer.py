"""customer.py - API calls for customer."""
from brainwave.models.customer import Customer
from brainwave import db


class CustomerAPI:
    """The API for customer manipulation."""
    @staticmethod
    def create(customer_dict):
        """Create a new customer."""
        customer = Customer.new_dict(customer_dict)

        db.session.add(customer)
        db.session.commit()

        return customer

    @staticmethod
    def update(customer_dict):
        """Update a customer."""
        customer = Customer.merge_dict(customer_dict)

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
        return Customer.query.all()
