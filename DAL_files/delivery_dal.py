from sqlalchemy.orm import Session
from models.delivery import Delivery

class DeliveryDAL:
    @classmethod
    def create_delivery(cls, db: Session, **kwargs):
        """Create a new delivery task."""
        delivery = Delivery(**kwargs)
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
        return delivery

    @classmethod
    def get_delivery_by_id(cls, db: Session, delivery_id: str):
        """Retrieve a delivery by its ID."""
        return db.query(Delivery).filter(Delivery.delivery_id == delivery_id).first()

    @classmethod
    def update_delivery(cls, db: Session, delivery_id: str, **kwargs):
        """Update an existing delivery task."""
        delivery = cls.get_delivery_by_id(db, delivery_id)
        if not delivery:
            return None
        for key, value in kwargs.items():
            setattr(delivery, key, value)
        db.commit()
        db.refresh(delivery)
        return delivery

    @classmethod
    def delete_delivery(cls, db: Session, delivery_id: str):
        """Delete a delivery by its ID."""
        delivery = cls.get_delivery_by_id(db, delivery_id)
        if not delivery:
            return False
        db.delete(delivery)
        db.commit()
        return True
