from sqlalchemy.orm import Session
from models.order_confirmation import OrderConfirmation

class OrderConfirmationDAL:
    @classmethod
    def create_order_confirmation(cls, db: Session, **kwargs):
        """Create a new order confirmation."""
        order_confirmation = OrderConfirmation(**kwargs)
        db.add(order_confirmation)
        db.commit()
        db.refresh(order_confirmation)
        return order_confirmation

    @classmethod
    def get_order_confirmation_by_order_id(cls, db: Session, order_id: str):
        """Retrieve the order confirmation by order_id."""
        return db.query(OrderConfirmation).filter(OrderConfirmation.order_id == order_id).first()

    @classmethod
    def update_order_confirmation(cls, db: Session, confirmation_id: str, **kwargs):
        """Update an existing order confirmation."""
        order_confirmation = cls.get_order_confirmation_by_order_id(db, confirmation_id)
        if not order_confirmation:
            return None
        for key, value in kwargs.items():
            setattr(order_confirmation, key, value)
        db.commit()
        db.refresh(order_confirmation)
        return order_confirmation

    @classmethod
    def delete_order_confirmation(cls, db: Session, confirmation_id: str):
        """Delete an order confirmation."""
        order_confirmation = cls.get_order_confirmation_by_order_id(db, confirmation_id)
        if not order_confirmation:
            return False
        db.delete(order_confirmation)
        db.commit()
        return True
