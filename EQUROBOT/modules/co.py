import os
import stripe
from pyrogram import Client, filters
from EQUROBOT import app


@app.on_message(filters.command("co"))
def command_handler(client, message):
    # Get command arguments
    command_args = message.command[1:]  # Get arguments after the command

    if len(command_args) < 2:
        message.reply_text("Usage: /co <amount>$ <stripe_key>")
        return

    # Check if the first argument is a valid dollar amount
    amount_str = command_args[0]
    if not amount_str.endswith("$") or not amount_str[:-1].replace('.', '', 1).isdigit():
        message.reply_text("Please provide a valid amount (e.g., 0.6$).")
        return

    # Extract the amount
    amount = float(amount_str[:-1])  # Remove the '$' and convert to float

    # Get the Stripe secret key from the command arguments
    stripe_secret_key = command_args[1]
    
    # Set the Stripe API key
    stripe.api_key = stripe_secret_key

    # Create a checkout session
    checkout_url = create_checkout_session(amount)
    if checkout_url:
        message.reply_text(f"Checkout link generated: {checkout_url}")
    else:
        message.reply_text("Failed to create checkout session.")

def create_checkout_session(amount):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Your Product Name',
                        },
                        'unit_amount': int(amount * 100),  # Convert to cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='https://yourdomain.com/success',  # Replace with your success URL
            cancel_url='https://yourdomain.com/cancel',    # Replace with your cancel URL
        )
        return session.url
    except Exception as e:
        print(e)  # Log the exception for debugging
        return None
