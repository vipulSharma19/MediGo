# entity_controller.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.schemas import EntityCreate, EntityUpdate, Entity  # Assuming schemas are defined
from database import get_db  # Assuming you have a method to get the DB session
from DAL_files.entity_dal import EntityDAL

# Create APIRouter instance
router = APIRouter()

# Endpoint to create a new entity
@router.post("/entities/", response_model=Entity)
def create_entity(entity: EntityCreate, db: Session = Depends(get_db)):
    try:
        # Using EntityDAL to create the entity
        new_entity = EntityDAL.create_entity(db, **entity.dict())
        return new_entity
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to get an entity by ID
@router.get("/entities/{entity_id}", response_model=Entity)
def get_entity(entity_id: str, db: Session = Depends(get_db)):
    db_entity = EntityDAL.get_entity_by_id(db, entity_id)
    if db_entity is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    return db_entity

# Endpoint to update an existing entity
@router.put("/entities/{entity_id}", response_model=Entity)
def update_entity(entity_id: str, entity: EntityUpdate, db: Session = Depends(get_db)):
    try:
        db_entity = EntityDAL.update_entity(db, entity_id, **entity.dict(exclude_unset=True))
        if not db_entity:
            raise HTTPException(status_code=404, detail="Entity not found or update failed")
        return db_entity
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to delete an entity by ID
@router.delete("/entities/{entity_id}", response_model=dict)
def delete_entity(entity_id: str, db: Session = Depends(get_db)):
    result = EntityDAL.delete_entity(db, entity_id)
    if not result:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {"message": "Entity deleted successfully"}

