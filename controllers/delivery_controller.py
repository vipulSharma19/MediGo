from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from DAL_files import delivery_dal
from schemas import delivery_schemas

router = APIRouter()

@router.post("/deliveries/", response_model=delivery_schemas.Delivery)
def create_delivery(delivery: delivery_schemas.DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = delivery_dal.DeliveryDAL.create_delivery(db=db, **delivery.dict())
    return db_delivery


@router.get("/deliveries/{delivery_id}", response_model=delivery_schemas.Delivery)
def get_delivery(delivery_id: str, db: Session = Depends(get_db)):
    # Use class method to get the delivery by ID
    db_delivery = delivery_dal.DeliveryDAL.get_delivery_by_id(db, delivery_id)

    if db_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return db_delivery


@router.put("/deliveries/{delivery_id}", response_model=delivery_schemas.Delivery)
def update_delivery(delivery_id: str, delivery: delivery_schemas.DeliveryUpdate, db: Session = Depends(get_db)):
    db_delivery = delivery_dal.DeliveryDAL.update_delivery(db=db, delivery_id=delivery_id, **delivery.dict())
    if db_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return db_delivery

@router.delete("/deliveries/{delivery_id}", response_model=delivery_schemas.Delivery)
def delete_delivery(delivery_id: str, db: Session = Depends(get_db)):
    deleted = delivery_dal.DeliveryDAL.delete_delivery(db=db, delivery_id=delivery_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return {"message": "Delivery deleted successfully"}
