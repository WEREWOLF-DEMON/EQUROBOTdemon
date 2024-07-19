from pyrogram import Client, filters
import requests
from EQUROBOT import app

# Define the URL and proxy
url = "https://freechecker.hrk.dev/checker"
proxy = "proxy.proxyverse.io:9200:country-us-session-df073d4956f342a3bfe074d2f6415a47:a5a94a55-c0b7-4e60-9acd-5e5f3cf09d6c"

@app.on_message(filters.command("cvv"))
async def handle_cvv(client, message):
    # Extract card number from the command argument
    card_info = message.text.split(' ', 1)
    if len(card_info) < 2:
        await message.reply_text("Please provide card details in the format: `cc|mm|yyyy|cvv`")
        return
    
    card_number = card_info[1]
    
    params = {
        'cc': card_number,
        'proxy': proxy
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        response_data = response.json()

        if "error" not in response_data:
            payment_details = response_data.get('payment', {})
            invoice = payment_details.get('invoice', '--')
            payment_id = payment_details.get('payment', '--')
            amount = payment_details.get('amount', '--')
            currency = payment_details.get('currency', '--')
            
            response_text = (
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
            error_code = error_details.get('code', '--')
            decline_code = error_details.get('decline_code', '--')

            payment_details = response_data.get('payment', {})
            failed_reason_message = payment_details.get('message', {}).get('failed_reason_message', 'Your card was declined.')

            response_text = (
                "┏━━━━━━━⍟\n"
                "┃# DECLINED ❌\n"
                "┗━━━━━━━━━━━⊛\n"
                f"CARD:- {card_number}\n"
                f"RESPONSE:- {failed_reason_message}\n"
                f"Code: {error_code}\n"
                f"Decline Code: {decline_code}"
            )
    except requests.RequestException as e:
        response_text = f"An error occurred: {str(e)}"
    
    await message.reply_text(response_text)
    
