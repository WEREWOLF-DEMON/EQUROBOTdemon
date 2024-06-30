from pyrogram import Client, filters
import stripe
import re
from EQUROBOT import app


stripe.api_key = 'sk_live_v6hZVe0J4f3rShGDqOSiwh8v'

#app = Client("stripe_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("cpay"))
async def cpay(client, message):
    try:
        # Extract card details from the message
        command, card_details = message.text.split(' ', 1)
        card_number, exp_month, exp_year, cvc = card_details.split('|')
        
        # Validate card details format
        if not re.match(r'^\d{16}$', card_number):
            raise ValueError("Invalid card number. Must be 16 digits.")
        if not re.match(r'^\d{2}$', exp_month) or not (1 <= int(exp_month) <= 12):
            raise ValueError("Invalid expiration month. Must be 2 digits and between 01-12.")
        if not re.match(r'^\d{4}$', exp_year) or int(exp_year) < 2024:
            raise ValueError("Invalid expiration year. Must be 4 digits and not in the past.")
        if not re.match(r'^\d{3,4}$', cvc):
            raise ValueError("Invalid CVC. Must be 3 or 4 digits.")

        # Create a PaymentMethod
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": card_number,
                "exp_month": int(exp_month),
                "exp_year": int(exp_year),
                "cvc": cvc,
            },
        )

        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=2000,  # Amount in cents (e.g., $20.00)
            currency='usd',
            payment_method=payment_method.id,
            confirmation_method='automatic',
            confirm=True,
            error_on_requires_action=True
        )

        # Handle different payment statuses
        if intent.status == 'succeeded':
            await message.reply("Payment succeeded!")
        elif intent.status == 'requires_action':
            await message.reply("Payment requires additional action.")
        elif intent.status == 'requires_payment_method':
            await message.reply("Payment failed. Payment method is required.")
        else:
            await message.reply(f"Payment failed with status: {intent.status}")

    except stripe.error.CardError as e:
        # Handle declined card error
        await message.reply(f"Card error: {e.user_message}")
    except stripe.error.InvalidRequestError as e:
        # Handle invalid request error
        await message.reply(f"Invalid request: {e.user_message}")
    except stripe.error.AuthenticationError as e:
        # Handle authentication error
        await message.reply(f"Authentication error: {e.user_message}")
    except stripe.error.APIConnectionError as e:
        # Handle API connection error
        await message.reply(f"Network error: {e.user_message}")
    except stripe.error.StripeError as e:
        # Handle generic Stripe error
        await message.reply(f"Payment processing error: {e.user_message}")
    except ValueError as e:
        # Handle validation error
        await message.reply(str(e))
    except Exception as e:
        # Handle any other error
        await message.reply(f"An unexpected error occurred: {str(e)}")
