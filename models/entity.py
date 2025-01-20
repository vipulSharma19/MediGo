from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from database import Base
import uuid
#
# class Entity(Base):
#     __tablename__ = 'entities'
#
#     entity_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     entity_type = Column(String(255), nullable=False)
#     created_at = Column(TIMESTAMP, nullable=False)
#     updated_at = Column(TIMESTAMP, nullable=False)
#
#     @declared_attr
#     def entity_id(cls):
#         """Automatically create entity_id for child classes without needing back_populates"""
#         return Column(UUID(as_uuid=True), ForeignKey('entities.entity_id'))
#
#     @declared_attr
#     def created_at(cls):
#         return Column(TIMESTAMP, nullable=False)
#
#     @declared_attr
#     def updated_at(cls):
#         return Column(TIMESTAMP, nullable=False)

from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
from datetime import datetime

class Entity(Base):
    __tablename__ = 'entities'

    # Primary key
    entity_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Type of entity (e.g., user, order, etc.)
    entity_type = Column(String(255), nullable=False)

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)


    # # Relationships (defined in child models)
    # user = relationship("User", back_populates="parent_entity", uselist=False)  # One-to-one with User
    # store = relationship("Store", back_populates="parent_entity", uselist=False)  # One-to-one with Store
    # order = relationship("Order", back_populates="parent_entity", uselist=False)  # One-to-one with Order
