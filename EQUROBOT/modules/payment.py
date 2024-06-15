import requests
import re
import os
from pyrogram import Client, filters
from faker import Faker
from * import app

fake = Faker()

# Fetch Stripe secret key from environment variables
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

@app.on_message(filters.command("checkout", prefixes=["/", "."]))
async def get_checkout(_, message):
    checkout_url = message.text[len('.checkout '):].strip()
    if not checkout_url:
        return await message.reply_text('Please provide a valid Stripe checkout URL.')

    # Extract the checkout session ID from the URL
    session_id_match = re.search(r'cs_[a-zA-Z0-9]+', checkout_url)
    if not session_id_match:
        return await message.reply_text(f'Invalid checkout URL: {checkout_url}. Please provide a valid Stripe checkout URL.')

    session_id = session_id_match.group(0)
    
    # Fetch the checkout session details from Stripe
    headers = {
        'Authorization': f'Bearer {STRIPE_SECRET_KEY}',
    }
    response = requests.get(f'https://api.stripe.com/v1/checkout/sessions/{session_id}', headers=headers)
    
    if response.status_code != 200:
        return await message.reply_text(f'Failed to fetch the checkout session details. Status Code: {response.status_code}\nResponse: {response.text}')

    session = response.json()

    amount_total = session['amount_total'] / 100  # Convert to dollars
    currency = session['currency'].upper()

    await message.reply_text(f'Checkout Session ID: {session_id}\nAmount Due: {amount_total} {currency}\nUse /pay <card_number>|<mm>|<yy>|<cvv> to make the payment.')

@app.on_message(filters.command("pay", prefixes=["/", "."]))
async def pay_invoice(_, message):
    payment_details = message.text[len('.pay '):].strip()
    reply_msg = message.reply_to_message
    if reply_msg:
        payment_details = reply_msg.text.strip()

    x = re.findall(r'\d+', payment_details)
    if len(x) != 4:
        return await message.reply_text('Invalid card details format. Should be in the format: <card_number>|<mm>|<yy>|<cvv>')

    ccn = x[0]
    mm = x[1]
    yy = x[2]
    cvv = x[3]

    # Generate a fake customer
    name = fake.name()
    email = fake.email()

    # Create a payment method in Stripe
    payment_method_data = {
        'type': 'card',
        'card[number]': ccn,
        'card[exp_month]': mm,
        'card[exp_year]': yy,
        'card[cvc]': cvv,
        'billing_details[name]': name,
        'billing_details[email]': email
    }
    headers = {
        'Authorization': f'Bearer {STRIPE_SECRET_KEY}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payment_method_response = requests.post('https://api.stripe.com/v1/payment_methods', data=payment_method_data, headers=headers)
    payment_method = payment_method_response.json()

    if payment_method_response.status_code != 200:
        return await message.reply_text(f'Failed to create a payment method. Status Code: {payment_method_response.status_code}\nResponse: {payment_method_response.text}')

    if 'Checkout Session ID' in reply_msg.text:
        session_id_match = re.search(r'cs_[a-zA-Z0-9]+', reply_msg.text)
        if session_id_match:
            session_id = session_id_match.group(0)
            # Fetch the checkout session details from Stripe
            session_response = requests.get(f'https://api.stripe.com/v1/checkout/sessions/{session_id}', headers=headers)
            
            if session_response.status_code != 200:
                return await message.reply_text(f'Failed to fetch the checkout session details. Status Code: {session_response.status_code}\nResponse: {session_response.text}')

            session = session_response.json()
            amount_total = session['amount_total'] / 100  # Convert to dollars
            currency = session['currency'].upper()

            # Attempt to complete the checkout session
            payment_intent_id = session['payment_intent']
            pay_session_data = {
                'payment_method': payment_method['id']
            }
            pay_session_response = requests.post(f'https://api.stripe.com/v1/payment_intents/{payment_intent_id}/confirm', data=pay_session_data, headers=headers)
            pay_result = pay_session_response.json()

            if pay_session_response.status_code == 200 and pay_result['status'] == 'succeeded':
                await message.reply_text(f'Payment Successful!\nAmount Charged: {amount_total} {currency}')
            else:
                error_message = pay_result.get('error', {}).get('message', 'Payment Failed')
                await message.reply_text(f'Payment Failed.\nReason: {error_message}\nStatus Code: {pay_session_response.status_code}\nResponse: {pay_session_response.text}')
    else:
        await message.reply_text('Please reply to a checkout session message with the card details.')
