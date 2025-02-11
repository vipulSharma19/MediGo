# Create the router
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from DAL_files.user_dal import UserDAL
from DAL_files.order_dal import OrderDAL
from DAL_files.store_dal import StoreDAL
from DAL_files.delivery_dal import DeliveryDAL
from database import get_db
from logic.twilio import send_whatsapp_message
# from logic.payment import generate_payment_link
from tasks import *
from utils import llm
router = APIRouter()


class WhatsAppMessage(BaseModel):
    phone: str
    message: str


@router.post("/webhook/")
def whatsapp_webhook(data: WhatsAppMessage, db: Session = Depends(get_db)):
    user_id = data.phone  # 'phone' is your user_id
    message = data.message.strip().lower()

    try:
        user = UserDAL.get_user_by_id(db, user_id)

        if not user:
            send_whatsapp_message(user_id, "Hi! Please provide your name and address to register.")
            return {"message": "User registration initiated."}
        user_details = llm.parse_user_details(message)
        name = user_details.get("name")
        address = user_details.get("address")
        send_whatsapp_message(user_id, "Please share Medicine names & their quantity, or a prescription.")

        # if not user.address:
        #     send_whatsapp_message(user_id, "Please provide your address to proceed.")
        #     return {"message": "Requesting user address."}

        if "order" in message or "prescription" in message:
            # Call the create order task asynchronously
            order_id = create_order_task.delay(user_id, message)
            send_whatsapp_message(user_id, "Checking nearby stores for availability...")
            return {"message": "Order received, checking stores.", "order_id": order_id}

        order = OrderDAL.get_order_by_id(db, user_id)
        if not order:
            send_whatsapp_message(user_id, "You don't have an active order. Please place an order first.")
            return {"message": "No active orders found."}

        order_state = order.status  # Track the state of the order

        # Handle user responses based on order state
        if order_state == "pending":
            if message == "confirm":
                # Call the confirm order task asynchronously
                OrderDAL.update_order_status(db, order.order_id, "awaiting_payment")
                confirm_order_task.delay(order.id, user_id)
                return {"message": "Order confirmed, awaiting payment."}

        # elif order_state == "awaiting_payment":
        #     if message == "pay":
        #         # Call the make payment task asynchronously
        #         make_payment_task.delay(order.id, user_id)
        #         return {"message": "Payment link sent, please complete your payment."}

        elif order_state == "payment_in_progress":
            send_whatsapp_message(user_id, "Your payment is being processed.")
            return {"message": "Payment in progress."}

        elif order_state == "in_progress":
            # Call the create delivery task asynchronously
            create_delivery_task.delay(order.id, user_id)
            send_whatsapp_message(user_id, "Your order is on the way!")
            return {"message": "Delivery is in progress."}

        elif order_state == "delivered":
            send_whatsapp_message(user_id, "Your order has been delivered.")
            return {"message": "Order delivered."}

        # Handle the case when the user is placing a new order
        if "order" in message or "prescription" in message:
            order_id = create_order_task.delay(user_id, message)
            send_whatsapp_message(user_id, "Checking nearby stores for availability...")
            return {"message": "Order received, checking stores.", "order_id": order_id}

        return {"message": "Unhandled scenario."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
