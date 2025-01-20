from sqlalchemy import Column, UUID, String, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from models.entity import Entity
from models.orders import Order
from models.store import Store
from models.delivery_person import DeliveryPerson
import uuid
from database import Base

class Delivery(Base):  # Inheriting from Entity to have common fields
    __tablename__ = 'deliveries'

    delivery_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.order_id'), nullable=False)
    store_id = Column(UUID(as_uuid=True), ForeignKey('stores.store_id'), nullable=False)
    delivery_person_id = Column(UUID(as_uuid=True), ForeignKey('delivery_persons.delivery_person_id'), nullable=False)
    pickup_location = Column(String(255), nullable=False)
    delivery_location = Column(String(255), nullable=False)
    delivery_fee = Column(DECIMAL, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    # Relationships to other models
    store = relationship("Store", back_populates="deliveries")
    delivery_person = relationship("DeliveryPerson", back_populates="deliveries")
    # parent_entity = relationship("Entity", back_populates="users")
    orders = relationship("Order", back_populates="deliveries")
