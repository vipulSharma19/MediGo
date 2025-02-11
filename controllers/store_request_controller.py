from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()
pending_orders = []  # Store pending orders (Temporary Storage)
active_connections = {}


@router.post("/stores/{store_id}/orders")
async def send_medicine_request(store_id: str, medicines: list, user_id: str, name: str, address: str):
    """
    Send the medicine order request to the nearest store.
    """
    order = {
        "store_id": store_id,
        "user_id": user_id,
        "name": name,
        "address": address,
        "medicines": medicines,
        "status": "pending"
    }

    pending_orders.append(order)  # Store the order in memory

    return JSONResponse(content={"message": "Order sent to store", "order": order})


@router.get("/stores/{store_id}/orders")
async def get_medicine_request(store_id: str):
    """
    Fetch pending medicine orders for a store.
    """
    orders = [order for order in pending_orders if order["store_id"] == store_id and order["status"] == "pending"]
    return JSONResponse(content={"orders": orders})


@router.post("/stores/{store_id}/confirm")
async def confirm_order(store_id: str, user_id: str, available_medicines: list):
    """ Store confirms available medicines and notifies WebSocket clients. """
    for order in pending_orders:
        if order["store_id"] == store_id and order["user_id"] == user_id:
            order["status"] = "confirmed"
            order["available_medicines"] = available_medicines
            break

    # Notify WebSocket client
    websocket = active_connections.get(store_id)
    if websocket:
        await websocket.send_json(available_medicines)

    return JSONResponse(content={"message": "Order confirmed", "available_medicines": available_medicines})
