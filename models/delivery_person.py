from sqlalchemy import Column, String, UUID, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from models.entity import Entity  # Inheriting from Entity class
import uuid
from sqlalchemy import Column, UUID, ForeignKey, DECIMAL, String, TIMESTAMP
from database import Base

class DeliveryPerson(Base):  # Inheriting from Entity to have common fields
    __tablename__ = 'delivery_persons'

    delivery_person_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    vehicle_type = Column(String(50), nullable=False)
    vehicle_number = Column(String, nullable=True)  # New field for vehicle number
    vehicle_img = Column(String, nullable=True)  # New field for vehicle image (base64 string)
    license_photo = Column(String, nullable=True)  # New field for license photo (base64 string)
    rc = Column(String, nullable=True)  # New field for RC (base64 string)
    aadhar_govt_id = Column(String, nullable=True)  # New field for Aadhar/Govt ID (base64 string)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    # Relationship to Delivery model (one-to-many)
    deliveries = relationship("Delivery", back_populates="delivery_person")
    # parent_entity = relationship("Entity", back_populates="users")
