from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from DAL_files import order_confirmation_dal
from schemas import order_confirmation_schemas

router = APIRouter()

@router.post("/order-confirmation/", response_model=order_confirmation_schemas.OrderConfirmation)
def create_order_confirmation(order_confirmation: order_confirmation_schemas.OrderConfirmationCreate, db: Session = Depends(get_db)):
    db_order_confirmation = order_confirmation_dal.OrderConfirmationDAL.create_order_confirmation(db=db, **order_confirmation.dict())
    return db_order_confirmation

@router.get("/order-confirmation/{order_id}", response_model=order_confirmation_schemas.OrderConfirmation)
def get_order_confirmation(order_id: str, db: Session = Depends(get_db)):
    db_order_confirmation = order_confirmation_dal.OrderConfirmationDAL.get_order_confirmation_by_order_id(db=db, order_id=order_id)
    if db_order_confirmation is None:
        raise HTTPException(status_code=404, detail="Order Confirmation not found")
    return db_order_confirmation

@router.put("/order-confirmation/{confirmation_id}", response_model=order_confirmation_schemas.OrderConfirmation)
def update_order_confirmation(confirmation_id: str, order_confirmation: order_confirmation_schemas.OrderConfirmationUpdate, db: Session = Depends(get_db)):
    db_order_confirmation = order_confirmation_dal.OrderConfirmationDAL.update_order_confirmation(db=db, confirmation_id=confirmation_id, **order_confirmation.dict())
    if db_order_confirmation is None:
        raise HTTPException(status_code=404, detail="Order Confirmation not found")
    return db_order_confirmation

@router.delete("/order-confirmation/{confirmation_id}", response_model=order_confirmation_schemas.OrderConfirmation)
def delete_order_confirmation(confirmation_id: str, db: Session = Depends(get_db)):
    deleted = order_confirmation_dal.OrderConfirmationDAL.delete_order_confirmation(db=db, confirmation_id=confirmation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order Confirmation not found")
    return {"message": "Order Confirmation deleted successfully"}
