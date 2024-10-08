import time
import re
import requests
import json
import asyncio, threading 
import os
import random
import string
import tempfile
from EQUROBOT import app
from EQUROBOT.core.mongo import has_premium_access, check_keys
from config import OWNER_ID
from pyrogram import filters
from collections import defaultdict
from requests.exceptions import RequestException
from EQUROBOT.modules import sk_set

user_request_times = defaultdict(list)
amount = 2

def generate_short_id():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

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

def get_random_proxy():
    return {
        "http": random.choice(proxy_list),
        "https": random.choice(proxy_list)
    }

async def check_card(card_info, sk, pk):
    results = []
    last_response = ""

    for card in card_info:
        card = card.strip()
        if not card:
            continue

        split = re.split(r"[|/:]", card)
        if len(split) != 4:
            error_str = f"Invalid card details for `{card}`"
            results.append(f"❌ **{error_str}**")
            last_response = error_str
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
            proxy = get_random_proxy()

            response = requests.post(
                "https://api.stripe.com/v1/payment_methods",
                data=token_data,
                headers={
                    "Authorization": f"Bearer {pk}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                proxies=proxy
            )
        except RequestException as e:
            error_str = f"Error with card `{cc}`: {str(e)}"
            results.append(f"❌ **{error_str}**")
            last_response = error_str
            continue

        if response.status_code != 200:
            try:
                error_message = response.json().get("error", {}).get("message", "Unknown error")
            except json.JSONDecodeError:
                error_message = "Unknown error"

            if cc.startswith("6"):
                resp = "Your card is not supported."
            else:
                resp = f"{error_message} for `{card}`"

            results.append(
                f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n"
                f"𝗦𝘁𝗮𝘁𝘂𝘀: **Error**⚠️\n"
                f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n"
            )
            last_response = resp
            continue

        try:
            token_data_response = response.json()
            token_id = token_data_response.get("id", "")
            if not token_id:
                raise ValueError("Token ID not found.")
        except (json.JSONDecodeError, ValueError) as e:
            error_str = f"Token creation failed for `{card}`: {str(e)}"
            results.append(f"❌ **{error_str}**")
            last_response = error_str
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
                proxies=proxy,
            )
        except RequestException as e:
            error_str = f"Charge error for `{cc}`: {str(e)}"
            results.append(f"❌ **{error_str}**")
            last_response = error_str
            continue

        charges = response.text

        try:
            charges_dict = json.loads(charges)
            charge_error = charges_dict.get("error", {}).get("decline_code", "Unknown error")
            charge_message = charges_dict.get("error", {}).get("message", "No message available")
        except json.JSONDecodeError:
            charge_error = "Unknown error (Invalid JSON response)"
            charge_message = "No message available"

        if '"status": "succeeded"' in charges:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
            resp = "Charged 1$🔥"
        elif '"cvc_check": "pass"' in charges:
            status = "𝗟𝗶𝘃𝗲 ✅"
            resp = "CVV Live"
        elif "generic_decline" in charges:
            status = "Declined ❌"
            resp = "Generic Decline"
        elif "insufficient_funds" in charges:
            status = "𝗟𝗶𝘃𝗲 ✅"
            resp = "Insufficient funds 💰"
        elif "fraudulent" in charges:
            status = "Declined ❌"
            resp = "Fraudulent"
        elif "do_not_honor" in charges:
            status = "Declined ❌"
            resp = "Do Not Honor"
        elif '"code": "incorrect_cvc"' in charges:
            status = "𝗟𝗶𝘃𝗲 ✅"
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
            status = "𝗖𝗖𝗡 𝗟𝗶𝘃𝗲 ✅"
            resp = "Transaction Not Allowed"
        elif "authentication_required" in charges or "card_error_authentication_required" in charges:
            status = "𝗟𝗶𝘃𝗲 ✅"
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
        last_response = resp

    return "\n".join(results), last_response

async def handle_cards(client, message, cards_info, unique_id, sk, pk):
    user = message.from_user
    profile_link = f"https://t.me/{user.username}"
    fullname = f"{user.first_name} {user.last_name or ''}".strip()

    processing_msg = await message.reply_text(
        f"**Gate** ➜ 𝗠𝗮𝘀𝘀 𝗦𝗞 𝗕𝗮𝘀𝗲𝗱 𝟭$\n\n"
        f"**Total CC Input** ➜ {len(cards_info)}\n"
        f"**Response** ➜ This response will update after 30 cards check...\n"
        f"**Status** ➜ Processing ■□□□\n\n"
        f"**Live Cards** ➜ 0\n"
        f"**Dead** ➜ 0\n"
        f"**Total Checked cards** ➜ 0\n\n"
        f"**sᴇᴄʀᴇᴛ ᴋᴇʏ** ➜ `{unique_id}`\n"
        f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})\n",
        disable_web_page_preview=True,
    )

    live_cards = []
    dead_cards_count = 0
    total_checked_cards = 0
    last_response = ""
    animation_states = ["■□□□", "■■□□", "■■■□", "■■■■"]

    update_frequency = 30


    for i, card in enumerate(cards_info):
        total_checked_cards += 1
        status_text, last_response = await check_card([card], sk, pk)

        if any(keyword in status_text for keyword in ["𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅", "𝗟𝗶𝘃𝗲 ✅", "𝗖𝗖𝗡 𝗟𝗶𝘃𝗲 ✅"]):
            live_cards.append(card)
        else:
            dead_cards_count += 1

        if total_checked_cards % update_frequency == 0 or total_checked_cards == len(cards_info):
            animation = animation_states[(total_checked_cards // update_frequency) % len(animation_states)]

            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=processing_msg.id,
                text=(
                    f"**Gate** ➜ 𝗠𝗮𝘀𝘀 𝗦𝗞 𝗕𝗮𝘀𝗲𝗱 𝟭$\n\n"
                    f"**Total CC Input** ➜ {len(cards_info)}\n"
                    f"**Response** ➜ {last_response}\n"
                    f"**Status** ➜ Processing {animation}\n\n"
                    f"**Live Cards** ➜ {len(live_cards)}\n"
                    f"**Dead** ➜ {dead_cards_count}\n"
                    f"**Total Checked cards** ➜ {total_checked_cards}\n\n"
                    f"**sᴇᴄʀᴇᴛ ᴋᴇʏ** ➜ `{unique_id}`\n"
                    f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})\n"
                ),
                disable_web_page_preview=True,
            )

    total_card = len(cards_info)
    if live_cards:
        final_message = (
            f"**Total cards** ➜ {total_card}\n"
            f"**Live Cards** ➜ {len(live_cards)}\n"
            f"**Dead** ➜ {dead_cards_count}\n"
            f"**Status** ➜ Checked All ✅\n\n"
            f"**Get Live Cards** ➜ `/gethits xvvtxt_{unique_id}`\n"
            f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})"
        )
    else:
        final_message = (
            f"**Total cards** ➜ {total_card}\n\n"
            f"**Live Cards** ➜ {len(live_cards)}\n"
            f"**Dead** ➜ {dead_cards_count}\n"
            f"**Status** ➜ Checked All ✅\n\n"
            f"**Result** ➜ __No Live Cards Found__\n"
            f"**ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{fullname}]({profile_link})"
        )

    await processing_msg.delete()
    await message.reply_text(final_message, disable_web_page_preview=True)

    if live_cards:
        file_name = f"live_cards_{unique_id}.txt"
        temp_file_path = os.path.join(os.getcwd(), file_name)

        with open(temp_file_path, "w") as temp_file:
            temp_file.write("\n".join(live_cards))

        os.environ[f'LIVE_CARDS_FILE_{unique_id}'] = temp_file_path



@app.on_message(filters.command("xvvtxt", prefixes=[".", "/"]))
async def handle_check_card(client, message):
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply_text("Please reply to a text file with the `/xvvtxt` command.")
        return

    if message.reply_to_message.document.mime_type == "text/plain":
        try:
            file_path = await message.reply_to_message.download()
            with open(file_path, "r") as f:
                cards_info = f.read().splitlines()
            os.remove(file_path)
        except Exception as e:
            await message.reply_text(f"Failed to download or read the file: {str(e)}")
            return

        if message.from_user.id != OWNER_ID and len(cards_info) > 1000:
            await message.reply_text("You can check a maximum of 1000 cards from a text file.")
            return

        sk, pk, mt = await check_keys()
        if not sk or not pk:
            await message.reply("Secret keys are not set. Please set them first.")
            return

        if cards_info:
            unique_id = generate_short_id()
            thread = threading.Thread(target=lambda: asyncio.run(handle_cards(client, message, cards_info, unique_id, sk, pk)))
            thread.start()
            #await handle_cards(client, message, cards_info, unique_id, sk, pk)
        else:
            await message.reply_text("No card found in the document.")
    else:
        await message.reply_text("Please upload a plain text (.txt) file.")

@app.on_message(filters.command("gethits", prefixes=[".", "/"]))
async def get_live_cards(client, message):
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")
    
    if len(message.command) != 2:
        await message.reply_text("Please provide the unique ID in the format: /gethits xvvtxt_{unique_id}")
        return

    unique_id = message.command[1].replace("xvvtxt_", "")
    temp_file_path = os.getenv(f'LIVE_CARDS_FILE_{unique_id}')

    if temp_file_path and os.path.exists(temp_file_path):
        card_count = 0

        with open(temp_file_path, "r") as file:
            for line in file:
                if card_pattern.search(line):
                    card_count += 1

        with open(temp_file_path, 'rb') as file:
            await message.reply_document(
                document=file,
                caption=f"Live Cards Found {card_count}",
            )
        os.remove(temp_file_path)
        del os.environ[f'LIVE_CARDS_FILE_{unique_id}']
    else:
        await message.reply_text("__No Live key found__")
