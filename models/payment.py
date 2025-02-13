from sqlalchemy import Column, UUID, ForeignKey, DECIMAL, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, TIMESTAMP

from models.entity import Entity  # Inheriting from Entity class
from models.orders import Order  # Linking to the Order model
from models.user import User  # Linking to the User model
import uuid
from database import Base
from sqlalchemy import Column, String, DateTime, func


class Payment(Base):  # Inheriting from Entity to have common fields
    __tablename__ = 'payments'

    payment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.order_id'), nullable=False)
    user_id = Column(String(20), ForeignKey('users.user_id'), nullable=False)  # Change UUID to Integer
    amount = Column(DECIMAL, nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(50), nullable=False, default="pending")
    payment_timestamp = Column(TIMESTAMP, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships to other models
    orders = relationship("Order", back_populates="payments")
    user = relationship("User", back_populates="payments")  # Relationship to the User model
    # parent_entity = relationship("Entity", back_populates="users")
