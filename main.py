# from utils.llm import LLM
#
# llm = LLM()
#
# # Example Input
# raw_input = """
# Hi, I'm John Doe. I'd like to order 2 strips of Paracetamol 500mg, one bottle of Cough Syrup, and 3 boxes of Aspirin 300mg.
# Can you deliver them to my office at 789 Oak Avenue, Springfield?
# Please ensure it's delivered before 5 PM, and let me know the total cost. Also, if possible, include Vitamin C tablets in my order. Thanks!
# """
#
# # Parse the user input
# parsed_details = llm.parse_user_details(raw_input)
#
# print("Parsed Details:", parsed_details)


from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, Request, Depends
from database import get_db
from models import User, Order, Store, Delivery
from utils import llm
from controllers import user_controller, order_controller, store_controller, delivery_controller
import requests
from tasks import process_webhook_task

app = FastAPI()


class MessagePayload(BaseModel):
    details: Optional[str] = None  # Add 'details' key to match request body

@app.get("/")
async def home():
    return {"message": "Hello, this is the webhook setup"}

@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()  # Read the JSON request body
    print("Received:", body)
    return {"status": "success", "received": body}


# # WhatsApp Webhook to Receive Messages
# @app.post("/webhook")
# async def receive_message(request: Request):
#     body = await request.json()
#     # user_data=llm.LLM.parse_user_details()
#
#     user_id = body.get("Phone")
#     Name = body.get("name", "").lower()
#     longitude = body.get("long_longitude", "")
#     latitude = body.get("lat_latitude", "")
#     address = f"{latitude} {longitude}"  # Proper string formatting
#     user = user_controller.get_user(user_id=user_id)
#
#     if not user:
#         user_data = {
#             "phone": user_id,
#             "name": Name,
#             "address": address
#         }
#         return await user_controller.create_user(user_data)  # Passing JSON directly
#
# # @app.post("/webhook")
# # async def receive_message(request: Request):
# #     body = await request.json()
# #
# #     user_id = body.get("Phone")
# #     Name = body.get("name", "").lower()
# #     longitude = body.get("long_longitude", "")
# #     latitude = body.get("lat_latitude", "")
# #     address = f"{latitude} {longitude}"
# #
# #     user_data = {
# #         "phone": user_id,
# #         "name": Name,
# #         "address": address
# #     }
# #
# #     # Enqueue task to process user asynchronously
# #     process_webhook_task.delay(user_data)
# #
# #     return {"status": "processing_in_background"}
#
#
# # Step 1: Request User Details for New Users
# @app.post("/user_details")
# async def request_user_details(request: Request):
#     body = await request.json()
#     user_details=llm.LLM(body)
#     return {"User's details for delivery":user_details}
#
#
# # Step 2: Handle Order Initiation
# @app.post("/medicine_details")
# async def handle_order_initiation(request: Request):
#     body = await request.json()
#     user_id = body.get("user_id")
#     medicines=llm.LLM.parse_user_details(body)
#
#
#     return {"status": "awaiting_medicine_details"}
#
#
# # Step 3: Process Medicine Request
# @app.post("/process_order")
# async def process_order(request: Request):
#     body = await request.json()
#     phone_number = body.get("from")
#     medicines = body.get("text")
#
#     user = user_controller.get_user_by_phone(phone_number)
#     if not user:
#         return {"status": "user_not_found"}
#
#     order = order_controller.create_order(user.id, medicines)
#     send_whatsapp_message(phone_number, "We are checking availability...")
#
#     return await query_nearby_stores(order)
#
#
# # Step 4: Query Nearby Stores
# async def query_nearby_stores(order):
#     stores = store_controller.get_store(order.user.location)
#     for store in stores:
#         notify_store(store.phone, order.id, order.medicines)
#     return {"status": "store_query_sent"}
#
#
# # Step 5: Handle Store Availability
# @app.post("/store_response")
# async def store_response(request: Request):
#     body = await request.json()
#     store_id = body.get("store_id")
#     order_id = body.get("order_id")
#     available = body.get("available", False)
#
#     order = order_controller.get_order(order_id)
#     if available:
#         order_controller.update_order_status(order_id, "confirmed")
#         send_whatsapp_message(order.user.phone, "Your order is confirmed. Please type 'confirm' to proceed.")
#     else:
#         send_whatsapp_message(order.user.phone, "Medicine unavailable. Do you want alternatives?")
#
#     return {"status": "updated"}
#
#
# # Step 6: Handle User Confirmation
# @app.post("/confirm_order")
# async def confirm_order(request: Request):
#     body = await request.json()
#     phone_number = body.get("from")
#     message_text = body.get("text", "").lower()
#
#     if "confirm" in message_text:
#         order = order_controller.get_latest_order(phone_number)
#         order_controller.update_order_status(order.id, "confirmed")
#         assign_delivery(order)
#
#     return {"status": "order_confirmed"}
#
#
# # Step 7: Assign Delivery
# async def assign_delivery(order):
#     delivery_person = delivery_controller.find_nearest_delivery(order.user.location)
#     delivery_controller.assign_order(order.id, delivery_person.id)
#     send_whatsapp_message(delivery_person.phone, f"New order assigned: {order.id}")
#     return {"status": "delivery_assigned"}
#
#
# # Step 8: Handle Payment
# @app.post("/process_payment")
# async def process_payment(request: Request):
#     body = await request.json()
#     phone_number = body.get("from")
#     order = order_controller.get_latest_order(phone_number)
#
#     payment_link = generate_payment_link(order)
#     send_whatsapp_message(phone_number, f"Please complete your payment: {payment_link}")
#     return {"status": "payment_link_sent"}
#
#
# # Step 9: Handle Delivery Completion
# @app.post("/delivery_completed")
# async def delivery_completed(request: Request):
#     body = await request.json()
#     order_id = body.get("order_id")
#     order_controller.update_order_status(order_id, "delivered")
#     send_whatsapp_message(order_controller.get_order(order_id).user.phone, "Your order has been delivered!")
#     return {"status": "delivered"}
#
#
# # Step 10: Collect Feedback
# @app.post("/collect_feedback")
# async def collect_feedback(request: Request):
#     body = await request.json()
#     phone_number = body.get("from")
#     feedback = body.get("text")
#
#     order = order_controller.get_latest_order(phone_number)
#     order_controller.store_feedback(order.id, feedback)
#     return {"status": "feedback_received"}
#
#
# # Helper function to send WhatsApp messages
# # def send_whatsapp_message(phone_number, message):
# #     url = "https://api.aisensy.com/sendMessage"
# #     payload = {"phone": phone_number, "text": message}
# #     headers = {"Content-Type": "application/json", "Authorization": "Bearer YOUR_API_KEY"}
# #     requests.post(url, json=payload, headers=headers)
#
#
# # Helper function to notify stores
# def notify_store(phone_number, order_id, medicines):
#     message = f"New order received (Order ID: {order_id}). Medicines: {medicines}"
#     send_whatsapp_message(phone_number, message)
#
#
# # Helper function to generate payment link
# def generate_payment_link(order):
#     return f"https://paymentgateway.com/pay/{order.id}"
