import time
import re
import requests
import json
import random
from EQUROBOT  import app
import asyncio, threading, queue
from EQUROBOT.core.mongo import has_premium_access, check_keys
from pyrogram import filters
from collections import defaultdict
from requests.exceptions import RequestException
from EQUROBOT.modules import sk_set
from config import OWNER_ID


amount = 4
user_request_times = defaultdict(list)
CARD_PATTERN = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

proxy_list = [
    "http://tickets:proxyon145@107.172.229.182:12345",
    "http://tickets:proxyon145@104.160.17.116:12345",
    "http://tickets:proxyon145@198.46.172.86:12345",
    "http://tickets:proxyon145@50.3.137.165:12345",
    "http://tickets:proxyon145@162.212.170.77:12345",
    "http://tickets:proxyon145@23.94.251.43:12345",
    "http://tickets:proxyon145@162.212.170.252:12345",
    "http://tickets:proxyon145@104.206.81.209:12345",
    "http://tickets:proxyon145@23.104.162.39:12345",
    "http://tickets:proxyon145@192.227.241.115:12345",
]

async def check_card(card_info, message, sk, pk):
    results = []

    for card in card_info:
        card = card.strip()
        if not card:
            continue

        proxy = random.choice(proxy_list)
        proxies = {"http": proxy, "https": proxy}

        split = card.split("|")
        if len(split) != 4:
            results.append(f"❌ **Invalid card details** for `{card}`")
            continue

        cc, mes, ano, cvv = split

        token_data = {
            'type': 'card',
            "card[number]": cc,
            "card[exp_month]": mes,
            "card[exp_year]": ano,
            "card[cvc]": cvv,
        }

        try:
            response = requests.post(
                "https://api.stripe.com/v1/payment_methods",
                data=token_data,
                headers={
                    "Authorization": f"Bearer {pk}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                proxies=proxies,
            )
        except RequestException as e:
            results.append(f"❌ **Error with card `{cc}`: {str(e)}**")
            continue

        if response.status_code != 200:
            try:
                error_message = response.json().get("error", {}).get("message", "Unknown error")
            except json.JSONDecodeError:
                error_message = "Unknown error"

            resp = f"{error_message} for `{card}`"
            if cc.startswith("6"):
                resp = "Your card is not supported."

            results.append(
                f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n"
                f"𝗦𝘁𝗮𝘁𝘂𝘀: **Error**⚠️\n"
                f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n"
            )
            continue

        token_data = response.json()
        token_id = token_data.get("id", "")
        if not token_id:
            results.append(f"❌ **Token creation failed** for `{card}`\n")
            continue

        charge_data = {
            "amount": amount * 100,
            "currency": "usd",
            'payment_method_types[]': 'card',
            "description": "Charge for product/service",
            'payment_method': token_id,
            'confirm': 'true',
            'off_session': 'true'
        }

        try:
            response = requests.post(
                "https://api.stripe.com/v1/payment_intents",
                data=charge_data,
                headers={
                    "Authorization": f"Bearer {sk}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                proxies=proxies,
            )
        except RequestException as e:
            results.append(f"❌ **Charge error** for `{cc}`: {str(e)}")
            continue

        charges = response.text

        try:
            charges_dict = json.loads(charges)
            charge_error = charges_dict.get("error", {}).get("decline_code", "Unknown error")
            charge_message = charges_dict.get("error", {}).get("message", "No message available")
        except json.JSONDecodeError:
            charge_error = "Unknown error (Invalid JSON response)"
            charge_message = "No message available"

        if '"seller_message": "Payment complete."' in charges:
            status = "Approved ✅"
            resp = "Charged 1$🔥"
        elif '"cvc_check": "pass"' in charges:
            status = "LIVE ✅"
            resp = "CVV Live"
        elif "generic_decline" in charges:
            status = "Declined ❌"
            resp = "Generic Decline"
        elif "insufficient_funds" in charges:
            status = "LIVE ✅"
            resp = "Insufficient funds 💰"
        elif "fraudulent" in charges:
            status = "Declined ❌"
            resp = "Fraudulent"
        elif "do_not_honor" in charges:
            status = "Declined ❌"
            resp = "Do Not Honor"
        elif '"code": "incorrect_cvc"' in charges:
            status = "LIVE ✅"
            resp = "Security code (CVC) is Incorrect."
        elif "invalid_expiry_month" in charges:
            status = "Declined ❌"
            resp = "The card expiration date provided is invalid."
        elif "invalid_account" in charges:
            status = "Declined ❌"
            resp = "The account linked to the card is invalid."
        elif "lost_card" in charges:
            status = "Declined ❌"
            resp = "The card has been reported as lost and the transaction was declined."
        elif "stolen_card" in charges:
            status = "Declined ❌"
            resp = "The card has been reported as stolen and the transaction was declined."
        elif "transaction_not_allowed" in charges:
            status = "CCN LIVE ✅"
            resp = "Transaction Not Allowed"
        elif "authentication_required" in charges or "card_error_authentication_required" in charges:
            status = "LIVE ✅"
            resp = "3D Secured"
        elif "pickup_card" in charges:
            status = "Declined ❌"
            resp = "Pickup Card"
        elif "Your card has expired." in charges:
            status = "Declined ❌"
            resp = "Expired Card"
        elif "card_decline_rate_limit_exceeded" in charges:
            status = "Declined ❌"
            resp = "Rate limit"
        elif '"code": "processing_error"' in charges:
            status = "Declined ❌"
            resp = "Processing error"
        elif '"message": "Your card number is incorrect."' in charges:
            status = "Declined ❌"
            resp = "Your card number is incorrect."
        elif "incorrect_number" in charges:
            status = "Declined ❌"
            resp = "Card number is invalid."
        elif "testmode_charges_only" in charges:
            status = "Declined ❌"
            resp = "The SK key is in test mode or invalid. Please use a valid key."
        elif "api_key_expired" in charges:
            status = "Declined ❌"
            resp = "The API key used for the transaction has expired."
        elif "parameter_invalid_empty" in charges:
            status = "Declined ❌"
            resp = "Please enter valid card details to check."
        else:
            status = f"{charge_error}"
            resp = f"{charge_message}"
            
        results.append(
            f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n"
            f"𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n"
            f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n"
        )

    return "\n".join(results)


@app.on_message(filters.command("xxvv", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id
    
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    

    try:
        card_info_text = (message.reply_to_message.text if message.reply_to_message else message.text)
        cards_info = card_info_text.split(maxsplit=1)[1].strip().split("\n") if len(card_info_text.split(maxsplit=1)) > 1 else None
    except IndexError:
        await message.reply(
            "Please provide multiple card details, each on a new line in the format: `card_number|mm|yy|cvv`"
        )
        return

    for card_info in cards_info:
        if not CARD_PATTERN.fullmatch(card_info.strip()):
            await message.reply(
                "Please provide the card details in the format: `card_number|mm|yy|cvv`."
            )
            return

    card_limit = 80

    if len(cards_info) > card_limit:
        await message.reply(
            f"You can check up to {card_limit} cards at a time. Please reduce the number of cards."
        )
        return

    sk, pk, mt = await check_keys()

    if not sk or not pk:
        await message.reply("Secret keys are not set. Please set them first.")
        return

    processing_msg = await message.reply("Processing your request...")

    start_time = time.time()

    try:
        response_queue = queue.Queue()
        thread = threading.Thread(target=lambda: response_queue.put(asyncio.run(check_card(cards_info, message, sk, pk))))
        thread.start()
        thread.join()
        response = response_queue.get()
        #response = await check_card(cards_info, message, sk, pk)
        elapsed_time = round(time.time() - start_time, 2)

        await processing_msg.edit_text(
            text=f"𝗠𝗮𝘀𝘀 𝗦𝗸 𝗕𝗮𝘀𝗲 **1$**\n\n{response}\n"
            f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
            f"𝗧𝗶𝗺𝗲: {elapsed_time} seconds"
        )
    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
