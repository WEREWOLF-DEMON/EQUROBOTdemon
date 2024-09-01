from pyrogram import Client, filters
import requests
from EQUROBOT import app



@app.on_message(filters.command("chk") & filters.reply)
async def check_card(client, message):
    card_number = message.text.split(" ", 1)[1].strip()  # Extract card number from the command
    if not card_number:
        await message.reply("Please provide a card number.")
        return
    
    # Send progress update
    await message.reply("Processing your card, please wait...")
    
    # Make API request (update with your API endpoint)
    url = f"https://mrdaxx.com/api.php?lista={card_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text

        # Construct and send response
        response_message = f"**\n┏━━━━━━━⍟\n┃#{card_number} $ \n┗━━━━━━━━━━━⊛\nCARD:- {card_number}\nRESPONSE:- {data}\nMSG:- Your card status is {data}\n**"
        await message.reply(response_message)
        
    except requests.exceptions.HTTPError as http_err:
        await message.reply(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        await message.reply(f"Request error occurred: {req_err}")
