"""credit.py - Controller calls for credit."""
from brainwave import db
from brainwave.models.credit import Credit
from brainwave.controllers.customer import CustomerController
from brainwave.controllers.association import AssociationController


class CreditController:
    """The controller for credit manipulation."""
    @staticmethod
    def create(credit_dict):
        """Create a credit for a customer of an association."""
        customer_id = credit_dict['customer_id']
        customer = CustomerController.get(customer_id)

        association_id = credit_dict['association_id']
        association = AssociationController.get(association_id)

        if not CustomerController.association_is_coupled(customer,
                                                         association):
            raise CustomerController.AssociationNotCoupled()

        credit = Credit.new_dict(credit_dict)
        db.session.add(credit)
        db.session.commit()

        return credit

    @staticmethod
    def get(credit_id):
        """Get a credit through its id."""
        return Credit.query.get(credit_id)

    @staticmethod
    def add(credit, amount):
        """Add to the credit."""
        credit.credit += amount
        db.session.add(credit)
        db.session.commit()

    @staticmethod
    def delete(credit):
        """Remove a credit."""
        db.session.delete(credit)
        db.session.commit()
