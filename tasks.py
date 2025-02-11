import logging
from celery import shared_task
from logic.twilio import send_whatsapp_message
from DAL_files.order_dal import OrderDAL
from DAL_files.store_dal import StoreDAL
from DAL_files.user_dal import UserDAL
# from logic.payment import generate_payment_link
from DAL_files.delivery_dal import DeliveryDAL

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from celery_config import app
from controllers import user_controller


@app.task
def process_webhook_task(user_data):
    """Background task to process webhook data"""
    user_id = user_data["phone"]
    user = user_controller.get_user(user_id=user_id)

    if not user:
        user_controller.create_user(user_data)

    return {"status": "user_processed"}


@shared_task
def create_user_task(user_id, name, address):
    try:
        user = UserDAL.create_user(user_id=user_id, name=name, address=address)
        print(f"User created {user}")
    except Exception as e:
        logger.error(f"Error in create_user_task: {e}")
        print(user_id, "There was an error registering your account. Please try again later.")
        raise e

@shared_task
def create_order_task(user_id, order_details):
    try:
        order_data = OrderDAL.create_order(user_id=user_id, order_details=order_details)
        order_id = order_data.get('order_id')
        if not order_id:
            raise ValueError("Order ID not returned from create_order.")
        send_whatsapp_message(user_id, "Your order has been created successfully.")
        return order_id
    except Exception as e:
        logger.error(f"Error in create_order_task: {e}")
        send_whatsapp_message(user_id, "There was an error creating your order. Please try again.")
        raise e

@shared_task
def check_store_availability(order_id, user_id):
    try:
        available_stores = StoreDAL.query_nearby_stores(order_id)
        if available_stores:
            store_list = ", ".join([store.name for store in available_stores])
            send_whatsapp_message(user_id, f"Your medicine is available at: {store_list}. Type 'confirm' to proceed.")
        else:
            send_whatsapp_message(user_id, "Sorry, no stores have your medicine at the moment. Would you like us to notify you when it becomes available?")
    except Exception as e:
        logger.error(f"Error in check_store_availability: {e}")
        send_whatsapp_message(user_id, "There was an issue checking store availability. Please try again later.")
        raise e

@shared_task
def confirm_order_task(order_id, user_id):
    try:
        OrderDAL.update_order(order_id, "confirmed")
        send_whatsapp_message(user_id, "Your order is confirmed.")
    except Exception as e:
        logger.error(f"Error in confirm_order_task: {e}")
        send_whatsapp_message(user_id, "There was an issue confirming your order. Please try again.")
        raise e

# @shared_task
# def make_payment_task(order_id, user_id):
#     try:
#         payment_link = generate_payment_link(order_id)
#         send_whatsapp_message(user_id, f"Complete your payment by clicking here: {payment_link}")
#     except Exception as e:
#         logger.error(f"Error in make_payment_task: {e}")
#         send_whatsapp_message(user_id, "There was an issue generating your payment link. Please try again.")
#         raise e

@shared_task
def create_delivery_task(order_id, user_id):
    try:
        delivery_person = DeliveryDAL.create_delivery(order_id)
        if not delivery_person:
            raise ValueError("No delivery person assigned.")
        send_whatsapp_message(user_id, f"Your order will be delivered by {delivery_person.name}.")
    except Exception as e:
        logger.error(f"Error in create_delivery_task: {e}")
        send_whatsapp_message(user_id, "There was an issue with delivery assignment. Please try again.")
        raise e
