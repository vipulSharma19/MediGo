from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from DAL_files import order_dal
from schemas import order_schemas
router = APIRouter()

@router.post("/orders/", response_model=order_schemas.Order)
def create_order(order: order_schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = order_dal.OrderDAL.create_order(db=db, **order.dict())
    return db_order

@router.get("/orders/{order_id}", response_model=order_schemas.Order)
def get_order(order_id: str, db: Session = Depends(get_db)):
    db_order = order_dal.OrderDAL.get_order_by_id(db=db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/orders/{order_id}", response_model=order_schemas.Order)
def update_order(order_id: str, order: order_schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = order_dal.OrderDAL.update_order(db=db, order_id=order_id, **order.dict())
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/orders/{order_id}", response_model=order_schemas.Order)
def delete_order(order_id: str, db: Session = Depends(get_db)):
    deleted = order_dal.OrderDAL.delete_order(db=db, order_id=order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}
