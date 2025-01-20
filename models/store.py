from sqlalchemy import Column, String, DateTime, Boolean, UUID
from sqlalchemy.orm import relationship
from models.entity import Entity  # Importing the Entity class to inherit from
import uuid
from sqlalchemy import Column, UUID, ForeignKey, DECIMAL, String, TIMESTAMP
from database import Base


class Store(Base):  # Now Store directly inherits from Entity
    __tablename__ = 'stores'

    store_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    proprietor_name = Column(String, nullable=True)  # New field for proprietor name
    dl_no = Column(String, nullable=True)  # New field for DL number
    dl_license_photo = Column(String, nullable=True)  # Base64-encoded DL license photo
    gst_pan_number = Column(String, nullable=True)  # New field for GST/PAN number
    gst_certificate_img = Column(String, nullable=True)  # Base64-encoded GST certificate
    govt_id = Column(String, nullable=True)  # New field for government ID (e.g., Aadhar)
    is_active = Column(Boolean, default=True)  # Field to mark if the store is active


    # parent_entity = relationship("Entity", back_populates="users")

    # No need to explicitly define the relationship here
    orders = relationship("Order", back_populates="store")
    deliveries = relationship("Delivery", back_populates="store")