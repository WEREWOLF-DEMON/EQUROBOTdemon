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
    if response_json.get('status') == 'success':
        reply_text = (
            "┏━━━━━━━⍟\n"
            f"┃#CHARGE {response_json.get('charge', 'UNKNOWN')} ✅\n"
            "┗━━━━━━━━━━━⊛\n"
            f"CARD:- {card_details}\n"
            f"RESPONSE:- {response_json.get('response', 'UNKNOWN')} ✅\n"
            f"MSG:- {response_json.get('message', 'PAYMENT SUCCESSFUL')} ✅"
        )
    else:
        reply_text = (
            "┏━━━━━━━⍟\n"
            "┃#DEAD ❌\n"
            "┗━━━━━━━━━━━⊛\n"
            f"CARD:- {card_details}\n"
            f"RESPONSE:- {response_json.get('response', 'UNKNOWN')} ❌\n"
            f"MSG:- {response_json.get('message', 'PAYMENT FAILED')} ❌"
        )
    
    # Send the response to the user
    await message.reply_text(reply_text)
