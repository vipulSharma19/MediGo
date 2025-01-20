from sqlalchemy.orm import Session
from models.user import User

class UserDAL:
    @classmethod
    def create_user(cls, db: Session, **kwargs):
        """Create a new user record."""
        user = User(**kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def get_user_by_id(cls, db: Session, user_id: str):
        """Retrieve a user by their ID."""
        return db.query(User).filter(User.user_id == user_id).first()

    @classmethod
    def update_user(cls, db: Session, user_id: str, **kwargs):
        """Update an existing user by their ID."""
        user = cls.get_user_by_id(db, user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def delete_user(cls, db: Session, user_id: str):
        """Delete a user by their ID."""
        user = cls.get_user_by_id(db, user_id)
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
