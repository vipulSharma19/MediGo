from sqlalchemy import Column, String, UUID, ForeignKey, Text, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from models.entity import Entity
import uuid
from sqlalchemy import Column, BigInteger, TIMESTAMP
from database import Base

class Order(Base):  # Inheriting from Entity
    __tablename__ = 'orders'

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medicine_names = Column(Text, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)  # Change UUID to Integer
    store_id = Column(UUID(as_uuid=True), ForeignKey('stores.store_id'), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    total_amount = Column(DECIMAL, nullable=False)
    payment_status = Column(String(50), nullable=False, default="pending")
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    # Relationship to Store model (allowing access to store details)
    # store = relationship("Store", back_populates="orders")
    # order_confirmation = relationship("OrderConfirmation", back_populates="order", uselist=False)
    # parent_entity = relationship("Entity", back_populates="users")
    user = relationship("User", back_populates="orders")

    # Relationship to Store model
    store = relationship("Store", back_populates="orders")
    payments = relationship("Payment", back_populates="orders")
    order_confirmation = relationship("OrderConfirmation", back_populates="orders")

    deliveries = relationship("Delivery", back_populates="orders")

