import time
import re
import asyncio
import requests
import json
from Flash import app
from pyrogram import Client, filters
import aiohttp
from requests.auth import HTTPBasicAuth
from collections import defaultdict
from requests.exceptions import RequestException

user_request_times = defaultdict(list)

ADMIN_IDS = [7019293589, 7044783841, 6757745933]

pk = "pk_live_51PpRSsGjCe9g75GWVyLe9Kjw0UVSQahdxJdHNez4xJlvXl1Dy5gOhU6yBx7wAaJJWMp4i7cJ6etPM6RpgMrBKskE00aPjIrsEh"
sk = "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"

async def check_card(card_info, message):
    results = []

    for card in card_info:
        card = card.strip()
        if not card:
            continue

        split = card.split("|")
        if len(split) != 4:
            results.append(f"❌ **Invalid card details** for `{card}`")
            continue

        cc, mes, ano, cvv = split

        token_data = {
            "card[number]": cc,
            "card[exp_month]": mes,
            "card[exp_year]": ano,
            "card[cvc]": cvv,
        }

        try:
            response = requests.post(
                "https://api.stripe.com/v1/tokens",
                data=token_data,
                headers={
                    "Authorization": f"Bearer {pk}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
        except RequestException as e:
            results.append(f"❌ **Error with card `{cc}`: {str(e)}**")
            continue

        if response.status_code != 200:
            results.append(
                f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n"
                f"𝗦𝘁𝗮𝘁𝘂𝘀: **Declined** ❌\n"
                f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: SK KEY REVOKED\n"
            )
            continue

        token_data = response.json()
        token_id = token_data.get("id", "")
        if not token_id:
            results.append(f"❌ **Token creation failed** for `{card}`")
            continue

        charge_data = {
            "amount": 100,
            "currency": "usd",
            "source": token_id,
            "description": "Charge for product/service",
        }

        try:
            response = requests.post(
                "https://api.stripe.com/v1/charges",
                data=charge_data,
                headers={
                    "Authorization": f"Bearer {sk}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
        except RequestException as e:
            results.append(f"❌ **Charge error** for `{cc}`: {str(e)}")
            continue

        chares = response.json()

        if response.status_code == 200 and chares.get("status") == "succeeded":
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱✅"
            resp = "Charged 1$ 🔥"
        elif "Your card's security code is incorrect." in json.dumps(chares):
            status = "𝗖𝗖𝗡 𝗟𝗶𝘃𝗲✅"
            resp = "Your card's security code is incorrect."
        elif "insufficient funds" in json.dumps(chares):
            status = "𝗖𝗩𝗩 𝗟𝗶𝘃𝗲✅"
            resp = "Your Card has Insufficient funds."
        else:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱❌"
            resp = chares.get("error", {}).get(
                "decline_code", chares.get("error", {}).get("message", "Unknown error")
            )

        results.append(
            f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n"
            f"𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n"
            f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n"
        )

    return "\n".join(results)


def check_user_limit(user_id):
    if user_id in ADMIN_IDS:
        return True, 0

    current_time = time.time()
    user_request_times[user_id] = [
        t for t in user_request_times[user_id] if current_time - t < 20
    ]

    if len(user_request_times[user_id]) >= 2:
        time_diff = 20 - (current_time - user_request_times[user_id][0])
        return False, round(time_diff, 2)

    user_request_times[user_id].append(current_time)
    return True, 0


card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

@app.on_message(filters.command("xxvv", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id

    allowed, remaining_time = check_user_limit(user_id)

    if not allowed:
        await message.reply(
            f"🚫 **Anti-Spam** Detected! Please try again after {remaining_time} seconds."
        )
        return

    try:
        cards_info = message.text.split(maxsplit=1)[1].strip().split("\n")
    except IndexError:
        await message.reply(
            "Please provide multiple card details, each on a new line in the format: `card_number|mm|yy|cvv`"
        )
        return

    for card_info in cards_info:
        if not card_pattern.fullmatch(card_info.strip()):
            await message.reply(
                "Please provide the card details in the format: `card_number|mm|yy|cvv`."
            )
            return

    if user_id in ADMIN_IDS:
        card_limit = 80
    else:
        card_limit = 10

    if len(cards_info) > card_limit:
        await message.reply(
            f"You can check up to {card_limit} cards at a time. Please reduce the number of cards."
        )
        return

    processing_msg = await message.reply("Processing your request...")

    start_time = time.time()

    try:
        response = await check_card(cards_info, message)
        elapsed_time = round(time.time() - start_time, 2)

        await processing_msg.edit_text(
            text=f"𝗠𝗮𝘀𝘀 𝗦𝗸 𝗕𝗮𝘀𝗲 **1$**\n\n{response}\n"
                 f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                 f"𝗧𝗶𝗺𝗲: {elapsed_time} seconds"
        )
    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
