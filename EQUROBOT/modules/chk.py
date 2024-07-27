import requests
from pyrogram import Client, filters
from EQUROBOT import app

# Command to check card details
@app.on_message(filters.command("chk"))
def check_card(client, message):
    try:
        card_details = message.text.split()[1]  # Get card details from the message
    except IndexError:
        message.reply_text("Please provide card details in the format: /chk <card_details>")
        return
    
    proxy = "babelill:lilybeck@iplayer-ueg9g.getfoxyproxy.org:13129"
    
    # API request parameters
    url = "http://z.daxxteam.com:8080/checker"
    params = {
        'cc': card_details,
        'proxy': proxy
    }
    
    try:
        response = requests.get(url, params=params)
        response_data = response.json()

        if 'payment' in response_data:
            payment_data = response_data['payment']
            amount = payment_data['amount']
            currency = payment_data['currency']
            invoice = payment_data['invoice']
            payment_id = payment_data['payment']
            status = payment_data['status']
            message_text = payment_data['message']['text']
            failed_reason = payment_data['message'].get('failed_reason_message', 'UNKNOWN')
            failed_reason_code = payment_data['message'].get('failed_reason_code', 'UNKNOWN')
            
            if status == 'success':
                response_text = (
                    f"┏━━━━━━━⍟\n"
                    f"┃#APPROVED {amount / 100} {currency} ✅\n"
                    f"┗━━━━━━━━━━━⊛\n"
                    f"CARD:- {card_details}\n"
                    f"INVOICE:- {invoice}\n"
                    f"PAYMENT:- {payment_id}\n"
                    f"AMOUNT:- {amount} {currency}\n"
                    f"RESPONSE:- CVV CHARGE ✅\n"
                    f"MSG:- PAYMENT SUCCESSFUL ✅"
                )
            else:
                response_text = (
                    f"┏━━━━━━━⍟\n"
                    f"┃ CARD DECLINED ❌\n"
                    f"┗━━━━━━━━━━━⊛\n"
                    f"➩ CARD: {card_details}\n"
                    f"➩ RESPONSE: *Payment Declined!❌*\n"
                    f"➩ REASON: {failed_reason_code}\n"
                    f"➩ MESSAGE: {failed_reason}"
                )
        else:
            response_text = "Invalid response from the API."

        message.reply_text(response_text)
    except Exception as e:
        message.reply_text(f"Error: {e}")
