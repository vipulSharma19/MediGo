from sqlalchemy.orm import Session
from models.orders import Order

class OrderDAL:
    @classmethod
    def create_order(cls, db: Session, **kwargs):
        """Create a new order."""
        order = Order(**kwargs)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @classmethod
    def get_order_by_id(cls, db: Session, order_id: str):
        """Retrieve an order by its ID."""
        return db.query(Order).filter(Order.order_id == order_id).first()

    @classmethod
    def update_order(cls, db: Session, order_id: str, **kwargs):
        """Update an existing order by its ID."""
        order = cls.get_order_by_id(db, order_id)
        if not order:
            return None
        for key, value in kwargs.items():
            setattr(order, key, value)
        db.commit()
        db.refresh(order)
        return order

    @classmethod
    def delete_order(cls, db: Session, order_id: str):
        """Delete an order by its ID."""
        order = cls.get_order_by_id(db, order_id)
        if not order:
            return False
        db.delete(order)
        db.commit()
        return True
