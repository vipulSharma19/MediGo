import streamlit as st
import requests
import asyncio
import websockets
import json

BACKEND_URL = "http://localhost:8000"
# Input field for Store ID
STORE_ID = st.text_input("Enter Store ID", "")

st.title("📦 Store Order Management")

# Fetch pending orders
def get_pending_orders():
    response = requests.get(f"{BACKEND_URL}/stores/{STORE_ID}/orders")
    if response.status_code == 200:
        return response.json().get("orders", [])
    return []

# Function to send confirmed medicines
def confirm_order(user_id, available_medicines):
    response = requests.post(
        f"{BACKEND_URL}/stores/{STORE_ID}/confirm",
        json={"user_id": user_id, "available_medicines": available_medicines},
    )
    if response.status_code == 200:
        st.success("✅ Order confirmed successfully!")
    else:
        st.error("❌ Failed to confirm order!")

# UI to display and confirm pending orders
orders = get_pending_orders()
if not orders:
    st.write("✅ No pending orders.")
else:
    for order in orders:
        st.subheader(f"🛒 Order from {order['name']} ({order['user_id']})")
        st.write(f"📍 Address: {order['address']}")
        st.write(f"💊 Medicines Requested: {', '.join(order['medicines'])}")

        available_medicines = st.multiselect(
            "Select available medicines:", order["medicines"], key=order["user_id"]
        )

        if st.button(f"Confirm Order for {order['user_id']}", key=f"confirm_{order['user_id']}"):
            confirm_order(order["user_id"], available_medicines)

# WebSocket Listener (Real-time updates)
async def listen_for_updates():
    async with websockets.connect(f"ws://localhost:8000/ws/{STORE_ID}") as websocket:
        while True:
            try:
                data = await websocket.recv()
                st.sidebar.success(f"🔔 Update: {data}")  # Display notification in sidebar
            except:
                st.sidebar.error("❌ WebSocket Disconnected!")
                break

# Run WebSocket listener in the background

if STORE_ID:  # Only connect if STORE_ID is provided
    asyncio.run(listen_for_updates())
