import base64
from sqlalchemy.orm import Session
from models.store import Store
from sqlalchemy import text

class StoreDAL:
    @classmethod
    def encode_file_to_base64(cls, file) -> str:
        """Encode a file to a Base64 string."""
        return base64.b64encode(file.file.read()).decode("utf-8")

    @classmethod
    def create_store(cls, db: Session, **kwargs):
        """Create a new store record with Base64-encoded images."""
        for key in ["dl_license_photo", "gst_certificate_img"]:
            if key in kwargs and kwargs[key]:
                kwargs[key] = cls.encode_file_to_base64(kwargs[key])

        store = Store(**kwargs)
        db.add(store)
        db.commit()
        db.refresh(store)
        return store

    @classmethod
    def get_store_by_id(cls, db: Session, store_id: str):
        """Retrieve a store by its ID."""
        return db.query(Store).filter(Store.store_id == store_id).first()

    @classmethod
    def update_store(cls, db: Session, store_id: str, **kwargs):
        """Update an existing store record with Base64-encoded images."""
        store = cls.get_store_by_id(db, store_id)
        if not store:
            return None

        for key in ["dl_license_photo", "gst_certificate_img"]:
            if key in kwargs and kwargs[key]:
                kwargs[key] = cls.encode_file_to_base64(kwargs[key])

        for key, value in kwargs.items():
            setattr(store, key, value)

        db.commit()
        db.refresh(store)
        return store

    @classmethod
    def delete_store(cls, db: Session, store_id: str):
        """Delete a store by its ID."""
        store = cls.get_store_by_id(db, store_id)
        if not store:
            return False
        db.delete(store)
        db.commit()
        return True
      
    @classmethod
    def get_nearest_store(cls, db: Session, latitude: float, longitude: float):
        """Find the nearest store using PostGIS ST_DistanceSphere."""
        query = text("""
            SELECT store_id, name, address, phone, email, 
                   ST_DistanceSphere(location, ST_MakePoint(:longitude, :latitude)) AS distance
            FROM stores
            WHERE is_active = true
            ORDER BY distance
            LIMIT 3;
        """)
        result = db.execute(query, {"latitude": latitude, "longitude": longitude}).fetchone()

        if result:
            return {
                "store_id": result.store_id,
                "name": result.name,
                "address": result.address,
                "phone": result.phone,
                "email": result.email,
                "distance_meters": result.distance
            }
        return None
