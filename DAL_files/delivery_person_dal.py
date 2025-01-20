from sqlalchemy.orm import Session
from models.delivery_person import DeliveryPerson
import base64
class DeliveryPersonDAL:
    @classmethod
    def encode_file_to_base64(cls, file) -> str:
        """Encode a file to a Base64 string."""
        return base64.b64encode(file.file.read()).decode("utf-8")

    @classmethod
    def create_delivery_person(cls, db: Session, **kwargs):
        """Create a new delivery person profile with Base64-encoded images."""
        # Encode images to Base64 if they exist in kwargs
        for key in ["vehicle_img", "license_photo", "rc", "aadhar_govt_id"]:
            if key in kwargs and kwargs[key]:
                kwargs[key] = cls.encode_file_to_base64(kwargs[key])

        delivery_person = DeliveryPerson(**kwargs)
        db.add(delivery_person)
        db.commit()
        db.refresh(delivery_person)
        return delivery_person

    @classmethod
    def get_delivery_person_by_id(cls, db: Session, delivery_person_id: str):
        """Retrieve a delivery person by their ID."""
        return db.query(DeliveryPerson).filter(DeliveryPerson.delivery_person_id == delivery_person_id).first()

    @classmethod
    def update_delivery_person(cls, db: Session, delivery_person_id: str, **kwargs):
        """Update an existing delivery person's profile with Base64-encoded images."""
        delivery_person = cls.get_delivery_person_by_id(db, delivery_person_id)
        if not delivery_person:
            return None

        # Encode images to Base64 if they exist in kwargs
        for key in ["vehicle_img", "license_photo", "rc", "aadhar_govt_id"]:
            if key in kwargs and kwargs[key]:
                kwargs[key] = cls.encode_file_to_base64(kwargs[key])

        for key, value in kwargs.items():
            setattr(delivery_person, key, value)

        db.commit()
        db.refresh(delivery_person)
        return delivery_person

    @classmethod
    def delete_delivery_person(cls, db: Session, delivery_person_id: str):
        """Delete a delivery person by their ID."""
        delivery_person = cls.get_delivery_person_by_id(db, delivery_person_id)
        if not delivery_person:
            return False
        db.delete(delivery_person)
        db.commit()
        return True
