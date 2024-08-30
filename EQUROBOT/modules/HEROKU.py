from pyrogram import Client, filters
import aiohttp
import re
from EQUROBOT import app

# Global variable to store Heroku API key
heroku_api_key = None

# Command to ask for the Heroku API key
@app.on_message(filters.command("hpay"))
async def ask_heroku_key(client, message):
    global heroku_api_key
    heroku_api_key = None
    await message.reply_text("Please ENTER YOUR HEROKU API KEY")

# Message handler to receive the Heroku API key
@app.on_message(filters.group & filters.text & ~filters.command("trycc"))
async def receive_heroku_key(client, message):
    global heroku_api_key
    if heroku_api_key is None:
        heroku_api_key = message.text.strip()
        await message.reply_text(f"LOGIN SUCCESSFUL ✅\nHEROKU API KEY: {heroku_api_key[:5]}... logged in successfully.\n\nNow, please SEND YOUR CREDIT CARD DETAILS using /trycc command.")

# Command to process credit card details
@app.on_message(filters.command("trycc"))
async def process_card(client, message):
    global heroku_api_key
    
    if heroku_api_key is None:
        await message.reply_text("Please enter your Heroku API key first using /hpay.")
        return
    
    try:
        # Extract the CC details from the message
        card_details = message.text.split()[1]
        parts = re.split('[:|]', card_details)

        if len(parts) != 4:
            await message.reply_text("Invalid card format. Please use the format: `card_number:exp_month:exp_year:cvc`")
            return
        
        n, mm, yy, cvc = parts

        # Heroku API request
        heroku_url = "https://api.heroku.com/account/payment-method/client-token"
        heroku_headers = {
            'User-Agent': "Mozilla/5.0",
            'Accept': "application/vnd.heroku+json; version=3",
            'authorization': f"Bearer {heroku_api_key}",
            'origin': "https://dashboard.heroku.com",
            'referer': "https://dashboard.heroku.com/",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(heroku_url, headers=heroku_headers) as response:
                if response.status != 200:
                    await message.reply_text("Error retrieving token from Heroku API. Please check your API key.")
                    return

                token_data = await response.json()
                token = token_data.get('token')
                if not token:
                    await message.reply_text("Failed to retrieve the token from Heroku.")
                    return

                pi_match = re.search(r'(pi_[^_]+)', token)
                if not pi_match:
                    await message.reply_text("Failed to extract the payment intent ID.")
                    return

                pi = pi_match.group(1)

                # Stripe API requests
                stripe_url = "https://api.stripe.com/v1/payment_methods"
                stripe_payload = {
                    "type": "card",
                    "billing_details[name]": "Slayer Noob",
                    "billing_details[address][city]": "New York",
                    "billing_details[address][country]": "US",
                    "billing_details[address][line1]": "20 Avenue A",
                    "billing_details[address][postal_code]": "10009",
                    "billing_details[address][state]": "NY",
                    "card[number]": n,
                    "card[cvc]": cvc,
                    "card[exp_month]": mm,
                    "card[exp_year]": yy,
                    "key": "pk_live_51KlgQ9Lzb5a9EJ3IaC3yPd1x6i9e6YW9O8d5PzmgPw9IDHixpwQcoNWcklSLhqeHri28drHwRSNlf6g22ZdSBBff002VQu6YLn"
                }

                stripe_headers = {
                    'User-Agent': "Mozilla/5.0",
                    'Accept': "application/json",
                    'Content-Type': "application/x-www-form-urlencoded",
                    'origin': "https://js.stripe.com",
                    'referer': "https://js.stripe.com/",
                }

                async with session.post(stripe_url, data=stripe_payload, headers=stripe_headers) as response:
                    if response.status != 200:
                        await message.reply_text("Error creating payment method with Stripe API.")
                        return

                    stripe_data = await response.json()
                    payment_method_id = stripe_data.get('id')
                    if not payment_method_id:
                        await message.reply_text("Failed to retrieve payment method ID from Stripe.")
                        return

                    # Confirming the payment intent with the retrieved payment method ID
                    confirm_url = f"https://api.stripe.com/v1/payment_intents/{pi}/confirm"
                    confirm_payload = {
                        "payment_method": payment_method_id,
                        "expected_payment_method_type": "card",
                        "use_stripe_sdk": "true",
                        "key": "pk_live_51KlgQ9Lzb5a9EJ3IaC3yPd1x6i9e6YW9O8d5PzmgPw9IDHixpwQcoNWcklSLhqeHri28drHwRSNlf6g22ZdSBBff002VQu6YLn",
                        "client_secret": token
                    }

                    async with session.post(confirm_url, data=confirm_payload, headers=stripe_headers) as response:
                        if response.status == 200:
                            await message.reply_text("Payment processed successfully!")
                        else:
                            response_text = await response.text()
                            await message.reply_text(f"Payment failed: {response_text}")

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
