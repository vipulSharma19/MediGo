from sqlalchemy.orm import Session
from models.payment import Payment

class PaymentDAL:
    @classmethod
    def create_payment(cls, db: Session, **kwargs):
        """Create a new payment record."""
        payment = Payment(**kwargs)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @classmethod
    def get_payment_by_id(cls, db: Session, payment_id: str):
        """Retrieve a payment by its ID."""
        return db.query(Payment).filter(Payment.payment_id == payment_id).first()

    @classmethod
    def update_payment(cls, db: Session, payment_id: str, **kwargs):
        """Update an existing payment record."""
        payment = cls.get_payment_by_id(db, payment_id)
        if not payment:
            return None
        for key, value in kwargs.items():
            setattr(payment, key, value)
        db.commit()
        db.refresh(payment)
        return payment

    @classmethod
    def delete_payment(cls, db: Session, payment_id: str):
        """Delete a payment record."""
        payment = cls.get_payment_by_id(db, payment_id)
        if not payment:
            return False
        db.delete(payment)
        db.commit()
        return True
