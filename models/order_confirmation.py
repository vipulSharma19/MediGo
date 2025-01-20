from sqlalchemy import Column, UUID, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from models.orders import Order   # Import Order model to create a relationship
import uuid
from models.entity import Entity
from database import Base

class OrderConfirmation(Base):  # Inheriting from Entity to have common fields
    __tablename__ = 'order_confirmation'

    confirmation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(PGUUID(as_uuid=True), ForeignKey('orders.order_id'), nullable=False)
    confirmation_status = Column(String(50), nullable=False)
    confirmation_timestamp = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    # Relationship to the Order model
    orders = relationship("Order", back_populates="order_confirmation")
    # parent_entity = relationship("Entity", back_populates="users")

