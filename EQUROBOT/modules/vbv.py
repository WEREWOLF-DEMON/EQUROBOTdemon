from pyrogram import Client, filters
import random
from EQUROBOT import app

@app.on_message(filters.command(['vbv', 'VBV'], prefixes=['.', '/']))
def vbv_command(client, message):
    try:
        # Extract the credit card details from the message
        card_details = message.text.split()[1].strip()

        # Simulate the 3D Secure lookup process
        result = simulate_3d_secure_lookup(card_details)

        # Send the result back to the user
        client.send_message(chat_id=message.chat.id, text=str(result))

    except IndexError:
        client.send_message(chat_id=message.chat.id, text="Please provide credit card details in the format: cc|mm|yyyy|cvv")
    except Exception as e:
        client.send_message(chat_id=message.chat.id, text=f"Error: {str(e)}")

def simulate_3d_secure_lookup(card_details):
    # Simulate the 3D Secure verification process
    try:
        card_number, expiration_month, expiration_year, cvv = card_details.split('|')
        card_number = card_number.strip()
        expiration_month = expiration_month.strip()
        expiration_year = expiration_year.strip()
        cvv = cvv.strip()

        # Simulate authentication outcome
        authentication_outcome = random.choice(["authenticated", "not_authenticated", "attempted", "failed"])

        if authentication_outcome == "authenticated":
            return {"status": "authenticated", "message": "3D Secure authentication successful"}
        elif authentication_outcome == "not_authenticated":
            return {"status": "not_authenticated", "message": "3D Secure authentication not successful"}
        elif authentication_outcome == "attempted":
            return {"status": "attempted", "message": "3D Secure authentication attempted but not completed"}
        else:
            return {"status": "failed", "message": "3D Secure authentication failed"}

    except ValueError:
        return {"error": "Invalid card details format"}
