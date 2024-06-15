import requests
import re
from pyrogram import Client, filters
from faker import Faker
from EQUROBOT import app

fake = Faker()

# Replace this with your actual Stripe secret key
STRIPE_SECRET_KEY = 'your_stripe_secret_key'

@app.on_message(filters.command("invoice", prefixes=["/", "."]))
async def get_invoice(_, message):
    invoice_url = message.text[len('.invoice '):].strip()
    if not invoice_url:
        return await message.reply_text('Please provide a valid Stripe invoice URL.')

    # Extract the invoice ID from the URL
    invoice_id_match = re.search(r'/invoices/(inv_[a-zA-Z0-9]+)', invoice_url)
    if not invoice_id_match:
        return await message.reply_text(f'Invalid invoice URL: {invoice_url}. Please provide a valid Stripe invoice URL.')

    invoice_id = invoice_id_match.group(1)
    
    # Fetch the invoice details from Stripe
    headers = {
        'Authorization': f'Bearer {STRIPE_SECRET_KEY}',
    }
    response = requests.get(f'https://api.stripe.com/v1/invoices/{invoice_id}', headers=headers)
    invoice = response.json()
    
    if response.status_code != 200:
        return await message.reply_text('Failed to fetch the invoice details. Please try again later.')

    amount_due = invoice['amount_due'] / 100  # Convert to dollars
    currency = invoice['currency'].upper()

    await message.reply_text(f'Invoice ID: {invoice_id}\nAmount Due: {amount_due} {currency}\nUse /pay <card_number>|<mm>|<yy>|<cvv> to make the payment.')

@app.on_message(filters.command("checkout", prefixes=["/", "."]))
async def get_checkout(_, message):
    checkout_url = message.text[len('.checkout '):].strip()
    if not checkout_url:
        return await message.reply_text('Please provide a valid Stripe checkout URL.')

    # Extract the checkout session ID from the URL
    session_id_match = re.search(r'session_id=(cs_[a-zA-Z0-9]+)', checkout_url)
    if not session_id_match:
        return await message.reply_text(f'Invalid checkout URL: {checkout_url}. Please provide a valid Stripe checkout URL.')

    session_id = session_id_match.group(1)
    
    # Fetch the checkout session details from Stripe
    headers = {
        'Authorization': f'Bearer {STRIPE_SECRET_KEY}',
    }
    response = requests.get(f'https://api.stripe.com/v1/checkout/sessions/{session_id}', headers=headers)
    session = response.json()
    
    if response.status_code != 200:
        return await message.reply_text('Failed to fetch the checkout session details. Please try again later.')

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
        'card': {
            'number': ccn,
            'exp_month': mm,
            'exp_year': yy,
            'cvc': cvv
        },
        'billing_details': {
            'name': name,
            'email': email
        }
    }
    headers = {
        'Authorization': f'Bearer {STRIPE_SECRET_KEY}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payment_method_response = requests.post('https://api.stripe.com/v1/payment_methods', data=payment_method_data, headers=headers)
    payment_method = payment_method_response.json()

    if payment_method_response.status_code != 200:
        return await message.reply_text('Failed to create a payment method. Please check the card details and try again.')

    # Determine if the previous message is for an invoice or a checkout session
    if 'Invoice ID' in reply_msg.text:
        invoice_id_match = re.search(r'Invoice ID: (inv_[a-zA-Z0-9]+)', reply_msg.text)
        if invoice_id_match:
            invoice_id = invoice_id_match.group(1)
            # Fetch the invoice details from Stripe
            invoice_response = requests.get(f'https://api.stripe.com/v1/invoices/{invoice_id}', headers=headers)
            invoice = invoice_response.json()
            amount_due = invoice['amount_due'] / 100  # Convert to dollars
            currency = invoice['currency'].upper()

            # Attempt to pay the invoice
            pay_invoice_data = {
                'customer': invoice['customer'],
                'payment_method': payment_method['id'],
                'invoice': invoice_id
            }
            pay_invoice_response = requests.post('https://api.stripe.com/v1/invoices/pay', data=pay_invoice_data, headers=headers)
            pay_result = pay_invoice_response.json()

            if pay_invoice_response.status_code == 200 and pay_result['status'] == 'paid':
                await message.reply_text(f'Payment Successful!\nAmount Charged: {amount_due} {currency}')
            else:
                error_message = pay_result.get('error', {}).get('message', 'Payment Failed')
                await message.reply_text(f'Payment Failed.\nReason: {error_message}')
    elif 'Checkout Session ID' in reply_msg.text:
        session_id_match = re.search(r'Checkout Session ID: (cs_[a-zA-Z0-9]+)', reply_msg.text)
        if session_id_match:
            session_id = session_id_match.group(1)
            # Fetch the checkout session details from Stripe
            session_response = requests.get(f'https://api.stripe.com/v1/checkout/sessions/{session_id}', headers=headers)
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
                await message.reply_text(f'Payment Failed.\nReason: {error_message}')
    else:
        await message.reply_text('Please reply to an invoice or checkout session message with the card details.')
