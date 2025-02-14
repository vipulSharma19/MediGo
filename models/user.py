from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID
from models.entity import Entity
from sqlalchemy import Column, BigInteger, TIMESTAMP

import uuid
from sqlalchemy import Column, UUID, ForeignKey, DECIMAL, String, TIMESTAMP
from database import Base
class User(Base):
    __tablename__ = 'users'

    # user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(20), primary_key=True)  # Rename to user_id, store phone number
    name = Column(String(255), nullable=False)
    #phone = Column(String(20), nullable=False)
    # email = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    # password = Column(String(255), nullable=False)
    # Relationship to Payment model
    # Relationship to Order model
    orders = relationship("Order", back_populates="user")

    # Relationship to Payment model (Assuming Payment is defined elsewhere)
    payments = relationship("Payment", back_populates="user")

