from twilio.rest import Client

# Twilio credentials (use environment variables for security)
TWILIO_PHONE = "your_twilio_phone_number"
ACCOUNT_SID = "your_account_sid"
AUTH_TOKEN = "your_auth_token"

def send_whatsapp_message(to: str, message: str):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=f"whatsapp:{TWILIO_PHONE}",
        to=f"whatsapp:{to}"
    )
    return message.sid
