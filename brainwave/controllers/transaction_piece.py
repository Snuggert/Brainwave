"""transaction_piece.py - Controller calls for TransactionPieces."""
from brainwave import db
from brainwave.models import TransactionPiece


class TransactionPieceController:
    @staticmethod
    def create(dict):
        transaction_piece = TransactionPiece.new_dict(dict)

        db.session.add(transaction_piece)
        db.session.commit()

        return transaction_piece

    @staticmethod
    def get_all_from(trans_id):
        """ Get all TransactionPiece objects by their shared transaction_id """

        return TransactionPiece.query.filter(transaction_id=trans_id).all()
