from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

class BaseDAL:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def create(self, **kwargs):
        """Create a new record."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get_by_id(self, entity_id: str):
        """Retrieve a record by ID."""
        try:
            return self.db.query(self.model).filter(self.model.entity_id == entity_id).one()
        except NoResultFound:
            return None

    def update(self, entity_id: str, **kwargs):
        """Update a record by ID."""
        instance = self.get_by_id(entity_id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, entity_id: str):
        """Delete a record by ID."""
        instance = self.get_by_id(entity_id)
        if not instance:
            return False
        self.db.delete(instance)
        self.db.commit()
        return True
