from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from DAL_files import delivery_person_dal
from schemas import delivery_person_schemas
router = APIRouter()

@router.post("/delivery-persons/", response_model=delivery_person_schemas.DeliveryPerson)
def create_delivery_person(
    name: str,
    contact_number: str,
    vehicle_number: str = None,
    vehicle_img: UploadFile = File(None),
    license_photo: UploadFile = File(None),
    rc: UploadFile = File(None),
    aadhar_govt_id: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        # Create a dictionary of incoming fields
        data = {
            "name": name,
            "contact_number": contact_number,
            "vehicle_number": vehicle_number,
            "vehicle_img": vehicle_img,
            "license_photo": license_photo,
            "rc": rc,
            "aadhar_govt_id": aadhar_govt_id,
        }

        # Call the DAL to create the delivery person
        new_delivery_person = delivery_person_dal.DeliveryPersonDAL.create_delivery_person(db, **data)
        return new_delivery_person
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/delivery-persons/{delivery_person_id}", response_model=delivery_person_schemas.DeliveryPerson)
def get_delivery_person(delivery_person_id: str, db: Session = Depends(get_db)):
    db_delivery_person = delivery_person_dal.DeliveryPersonDAL.get_delivery_person_by_id(db=db, delivery_person_id=delivery_person_id)
    if db_delivery_person is None:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    return db_delivery_person

# Endpoint to update an existing delivery person
@router.put("/delivery-persons/{delivery_person_id}", response_model=delivery_person_schemas.DeliveryPerson)
def update_delivery_person(
    delivery_person_id: str,
    name: str = None,
    contact_number: str = None,
    vehicle_number: str = None,
    vehicle_img: UploadFile = File(None),
    license_photo: UploadFile = File(None),
    rc: UploadFile = File(None),
    aadhar_govt_id: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        # Create a dictionary of incoming fields
        data = {
            "name": name,
            "contact_number": contact_number,
            "vehicle_number": vehicle_number,
            "vehicle_img": vehicle_img,
            "license_photo": license_photo,
            "rc": rc,
            "aadhar_govt_id": aadhar_govt_id,
        }

        # Call the DAL to update the delivery person
        updated_delivery_person = delivery_person_dal.DeliveryPersonDAL.update_delivery_person(
            db, delivery_person_id, **{k: v for k, v in data.items() if v is not None}
        )
        if not updated_delivery_person:
            raise HTTPException(status_code=404, detail="Delivery person not found")
        return updated_delivery_person
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delivery-persons/{delivery_person_id}", response_model=delivery_person_schemas.DeliveryPerson)
def delete_delivery_person(delivery_person_id: str, db: Session = Depends(get_db)):
    deleted = delivery_person_dal.DeliveryPersonDAL.delete_delivery_person(db=db, delivery_person_id=delivery_person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    return {"message": "Delivery person deleted successfully"}
