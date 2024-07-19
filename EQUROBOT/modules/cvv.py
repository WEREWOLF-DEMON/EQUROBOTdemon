from pyrogram import Client, filters
import requests
from EQUROBOT import app

url = "https://freechecker.hrk.dev/checker"

@app.on_message(filters.command('.cvv'))
async def request_card_number(client, message):
    # Prompt the user to send their card number
    await message.reply_text("Please send your card number in the format: `cc|mm|yyyy|cvv`.")

@app.on_message(filters.text & filters.reply)
async def check_cvv(client, message):
    if message.reply_to_message and message.reply_to_message.text == "Please send your card number in the format: `cc|mm|yyyy|cvv`.":
        card_number = message.text.strip()

        params = {
            'cc': card_number,
            'proxy': "proxy.proxyverse.io:9200:country-us-session-df073d4956f342a3bfe074d2f6415a47:a5a94a55-c0b7-4e60-9acd-5e5f3cf09d6c"
        }

        response = requests.get(url, params=params)
        response_data = response.json()

        if response.status_code == 200 and "error" not in response_data:
            payment_details = response_data.get('payment', {})
            invoice = payment_details.get('invoice', 'N/A')
            payment_id = payment_details.get('payment', 'N/A')
            amount = payment_details.get('amount', 'N/A')
            currency = payment_details.get('currency', 'N/A')
            
            reply = (
                "┏━━━━━━━⍟\n"
                "┃#APPROVED 𝟓$ ✅\n"
                "┗━━━━━━━━━━━⊛\n"
                f"CARD:- {card_number}\n"
                f"INVOICE:- {invoice}\n"
                f"PAYMENT:- {payment_id}\n"
                f"AMOUNT:- {amount} {currency}\n"
                "RESPONSE:- CVV CHARGE ✅\n"
                "MSG:- PAYMENT SUCCESSFUL ✅"
            )
        else:
            error_details = response_data.get('details', {}).get('error', {})
            error_message = error_details.get('message', 'Your card was declined.')
            error_code = error_details.get('code', 'N/A')
            decline_code = error_details.get('decline_code', 'N/A')

            payment_details = response_data.get('payment', {})
            failed_reason_message = payment_details.get('message', {}).get('failed_reason_message', 'Your card was declined.')

            reply = (
                "┏━━━━━━━⍟\n"
                "┃# DECLINED ❌\n"
                "┗━━━━━━━━━━━⊛\n"
                f"CARD:- {card_number}\n"
                f"RESPONSE:- {failed_reason_message}\n"
                f"Code: {error_code}\n"
                f"Decline Code: {decline_code}"
            )
        
        await message.reply_text(reply)
