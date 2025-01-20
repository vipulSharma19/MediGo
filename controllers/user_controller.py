from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.user_schemas import UserCreate, UserUpdate, User  # Assuming schemas are already defined
from database import get_db  # Assuming you have a method to get the DB session
from DAL_files.user_dal import UserDAL

router = APIRouter()

# Endpoint to create a new user
@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Using UserDAL to create the user
        new_user = UserDAL.create_user(db, **user.dict())
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to get a user by ID
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = UserDAL.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Endpoint to update an existing user
@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = UserDAL.update_user(db, user_id, **user.dict(exclude_unset=True))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Endpoint to delete a user by ID
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    result = UserDAL.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
