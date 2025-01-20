from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from DAL_files import store_dal
from schemas import store_schemas
router = APIRouter()

@router.post("/stores/", response_model=store_schemas.Store)
def create_store(
    name: str,
    address: str,
    contact_number: str,
    proprietor_name: str = None,
    dl_no: str = None,
    dl_license_photo: UploadFile = File(None),
    gst_pan_number: str = None,
    gst_certificate_img: UploadFile = File(None),
    govt_id: str = None,
    db: Session = Depends(get_db),
):
    try:
        data = {
            "name": name,
            "address": address,
            "contact_number": contact_number,
            "proprietor_name": proprietor_name,
            "dl_no": dl_no,
            "dl_license_photo": dl_license_photo,
            "gst_pan_number": gst_pan_number,
            "gst_certificate_img": gst_certificate_img,
            "govt_id": govt_id,
        }
        new_store = store_dal.StoreDAL.create_store(db, **data)
        return new_store
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stores/{store_id}", response_model=store_schemas.Store)
def get_store(store_id: str, db: Session = Depends(get_db)):
    db_store = store_dal.StoreDAL.get_store_by_id(db=db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store

@router.put("/stores/{store_id}", response_model=store_schemas.Store)
def update_store(
    store_id: str,
    name: str = None,
    address: str = None,
    contact_number: str = None,
    proprietor_name: str = None,
    dl_no: str = None,
    dl_license_photo: UploadFile = File(None),
    gst_pan_number: str = None,
    gst_certificate_img: UploadFile = File(None),
    govt_id: str = None,
    db: Session = Depends(get_db),
):
    try:
        data = {
            "name": name,
            "address": address,
            "contact_number": contact_number,
            "proprietor_name": proprietor_name,
            "dl_no": dl_no,
            "dl_license_photo": dl_license_photo,
            "gst_pan_number": gst_pan_number,
            "gst_certificate_img": gst_certificate_img,
            "govt_id": govt_id,
        }
        updated_store = store_dal.StoreDAL.update_store(
            db, store_id, **{k: v for k, v in data.items() if v is not None}
        )
        if not updated_store:
            raise HTTPException(status_code=404, detail="Store not found")
        return updated_store
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/stores/{store_id}", response_model=store_schemas.Store)
def delete_store(store_id: str, db: Session = Depends(get_db)):
    deleted = store_dal.StoreDAL.delete_store(db=db, store_id=store_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Store not found")
    return {"message": "Store deleted successfully"}
