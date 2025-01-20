from sqlalchemy.orm import Session
from models.entity import Entity

class EntityDAL:
    @classmethod
    def create_entity(cls, db: Session, **kwargs):
        """Create a new entity record."""
        entity = Entity(**kwargs)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    @classmethod
    def get_entity_by_id(cls, db: Session, entity_id: str):
        """Retrieve an entity by its ID."""
        return db.query(Entity).filter(Entity.entity_id == entity_id).first()

    @classmethod
    def update_entity(cls, db: Session, entity_id: str, **kwargs):
        """Update an existing entity by its ID."""
        entity = cls.get_entity_by_id(db, entity_id)
        if not entity:
            return None
        for key, value in kwargs.items():
            setattr(entity, key, value)
        db.commit()
        db.refresh(entity)
        return entity

    @classmethod
    def delete_entity(cls, db: Session, entity_id: str):
        """Delete an entity by its ID."""
        entity = cls.get_entity_by_id(db, entity_id)
        if not entity:
            return False
        db.delete(entity)
        db.commit()
        return True
