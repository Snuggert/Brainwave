"""credit.py - Controller calls for credit."""
from brainwave import db
from brainwave.models.credit import Credit
from brainwave.controllers.customer import CustomerController


class CreditController:
    """The controller for credit manipulation."""
    @staticmethod
    def create(customer, association):
        """Create a credit for a customer of an association."""
        if not CustomerController.association_is_coupled(customer,
                                                         association):
            raise CustomerController.AssociationNotCoupled()

        credit = Credit(0.0, customer, association)
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
