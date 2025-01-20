from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from DAL_files import payment_dal
from schemas import payment_schemas
router = APIRouter()

@router.post("/payments/", response_model=payment_schemas.Payment)
def create_payment(payment: payment_schemas.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = payment_dal.PaymentDAL.create_payment(db=db, **payment.dict())
    return db_payment

@router.get("/payments/{payment_id}", response_model=payment_schemas.Payment)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    db_payment = payment_dal.PaymentDAL.get_payment_by_id(db=db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.put("/payments/{payment_id}", response_model=payment_schemas.Payment)
def update_payment(payment_id: str, payment: payment_schemas.PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = payment_dal.PaymentDAL.update_payment(db=db, payment_id=payment_id, **payment.dict())
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.delete("/payments/{payment_id}", response_model=payment_schemas.Payment)
def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    deleted = payment_dal.PaymentDAL.delete_payment(db=db, payment_id=payment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}
    