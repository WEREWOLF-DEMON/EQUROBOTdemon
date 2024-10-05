from EQUROBOT import app
from EQUROBOT.core.mongo import save_keys, delete_keys, check_keys
import logging
from pyrogram import filters
from config import OWNER_ID
import time
import requests
from requests.auth import HTTPBasicAuth


def retrieve_balance(sk):
    url = "https://api.stripe.com/v1/balance"
    auth = HTTPBasicAuth(sk, "")
    response = requests.get(url, auth=auth)
    return response.json()

def retrieve_publishable_key_and_merchant(sk):
    price_url = "https://api.stripe.com/v1/prices"
    headers = {"Authorization": f"Bearer {sk}"}
    price_data = {
        "currency": "usd",
        "unit_amount": 1000,
        "product_data[name]": "Gold Plan",
    }

    price_response = requests.post(price_url, headers=headers, data=price_data)
    if price_response.status_code != 200:
        error = price_response.json().get("error", {})
        code = error.get("code", "")
        message = error.get("message", "")

        if (
            code in ("api_key_expired", "payment_link_no_valid_payment_methods")
            or "Invalid API Key provided" in message
        ):
            raise Exception(f"{code}: {message}")

        raise Exception(f"{error.get('type', 'error')}: {message}")

    payment_link_url = "https://api.stripe.com/v1/payment_links"
    payment_link_data = {
        "line_items[0][quantity]": 1,
        "line_items[0][price]": price_response.json()["id"],
    }
    payment_link_response = requests.post(
        payment_link_url, headers=headers, data=payment_link_data
    )

    if payment_link_response.status_code != 200:
        error = payment_link_response.json().get("error", {})
        if error.get("code") == "payment_link_no_valid_payment_methods":
            return None, None
        raise Exception(f"Failed to create payment link: {payment_link_response.text}")

    payment_link_id = payment_link_response.json()["url"].split("/")[-1]
    merchant_response = requests.get(
        f"https://merchant-ui-api.stripe.com/payment-links/{payment_link_id}"
    )

    if merchant_response.status_code != 200:
        raise Exception(
            f"Failed to retrieve publishable key and merchant: {merchant_response.text}"
        )

    data = merchant_response.json()
    return data.get("key"), data.get("merchant")

async def check_status(message, sk, user_id):
    start_time = time.perf_counter()
    publishable_key, merchant = None, None
    status, resp = "SK Dead ❌", "Unknown error"

    try:
        publishable_key, merchant = retrieve_publishable_key_and_merchant(sk)
        if publishable_key:
            status = "SK Live ✅"
            resp = "This SK is live and functional."
        else:
            status = "Test Mode ⚙️"
            resp = "Your account cannot currently make live charges."
    except Exception as e:
        error_response = str(e)

        error_mapping = {
            "API Key Expired": ("SK Dead ❌", "API Key Expired"),
            "Expired API Key provided": ("SK Dead ❌", "Expired API Key"),
            "Invalid API Key": ("SK Dead ❌", "Invalid API Key"),
            "Account Country Not Supported": (
                "Integration Off ⚠️",
                "Account Country Not Supported",
            ),
            "Publishable Key Misuse": ("Test Mode ⚙️", "Publishable Key Misuse"),
            "Account Restricted from Live Charges": (
                "SK Dead ❌",
                "Account Restricted from Live Charges",
            ),
            "Account Not Activated": ("SK Dead ❌", "Account Not Activated"),
            "Rate Limit Exceeded": ("SK Rate Limited 🚨", "Rate Limit Exceeded"),
            "API Key Revoked": ("SK Dead ❌", "API Key Revoked"),
            "Permission Denied": ("Access Denied 🚫", "Permission Denied"),
            "Account Suspended": ("Account Suspended ⛔", "Account Suspended"),
            "Currency Not Supported": ("Integration Off ⚠️", "Currency Not Supported"),
            "Insufficient Permissions": ("Access Denied 🚫", "Insufficient Permissions"),
            "Invalid Request": ("Invalid Request 🚫", "Invalid Request"),
            "Duplicate Transaction": ("Transaction Error ⚠️", "Duplicate Transaction"),
            "Missing Required Parameter": (
                "Invalid Request 🚫",
                "Missing Required Parameter",
            ),
            "API Internal Error": ("Server Error ⚠️", "API Internal Error"),
            "Network Error": ("Network Issue 🌐", "Network Error"),
            "Payment Method Not Supported": (
                "Payment Issue ⚠️",
                "Payment Method Not Supported",
            ),
        }

        for error_message, (stat, response) in error_mapping.items():
            if error_message in error_response:
                status, resp = stat, response
                break

    balance_data = retrieve_balance(sk)

    if "rate_limit" in balance_data:
        status, resp = "**RATE LIMIT**⚠️", "Rate limit exceeded"

    try:
        available_balance = balance_data["available"][0]["amount"] / 100
        pending_balance = balance_data["pending"][0]["amount"] / 100
        currency = balance_data["available"][0]["currency"]
    except KeyError:
        available_balance, pending_balance, currency = (
            "Not Available",
            "Not Available",
            "Not Available",
        )

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    response_text = (
        "┏━━━━━━━⍟\n"
        "┃  **sᴋ ʟᴏᴏᴋᴜᴘ** ✅ \n"
        "┗━━━━━━━━━━━⊛\n\n"
        f"**⊙ SK Status** ➜ **{status}**\n"
        f"**⊙ Response** ➜ {resp}\n\n"
        f"**⊙ SK Key** ➜ `{sk}`\n"
        f"**⊙ Publishable Key** ➜ `{publishable_key or 'Not Available'}`\n"
        f"**⊙ Currency** ➜ {currency}\n"
        f"**⊙ Available Balance** ➜ {available_balance}$\n"
        f"**⊙ Pending Balance** ➜ {pending_balance}$\n"
        f"**⊙ Time Taken** ➜ {elapsed_time:.2f} seconds\n"
        f"**⊙ ᴄʜᴇᴄᴋᴇᴅ ʙʏ** ➜ [{message.from_user.first_name}](tg://user?id={user_id})"
    )

    return response_text

@app.on_message(filters.command("setsk", prefixes=["/", ".", "!"]))
async def set_sk(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to set the secret key.")
        return

    try:
        sk = message.text.split(' ', 1)[1]
        pk, merchant = retrieve_publishable_key_and_merchant(sk)

        await save_keys(sk, pk, merchant)

        if not pk:
            result_text = await check_status(message, sk, message.from_user.id)
            await message.reply(result_text)
        else:
            logging.info(f"Secret key and publishable key set by {message.from_user.id}")
            await message.reply(f"Secret key and publishable key have been set successfully.\n**Publishable Key**: `{pk}`")

    except IndexError:
        await message.reply("Please provide a valid key after the command. Example: /setsk sk_live_123")
    except Exception as e:
        await message.reply(f"Failed to retrieve publishable key or merchant: {str(e)}")

@app.on_message(filters.command("removesk", prefixes=["/", ".", "!"]))
async def remove_sk(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to remove the secret key.")
        return

    sk, pk, mt = await check_keys()
    if sk:
        await delete_keys()
        logging.info(f"Secret key removed by {message.from_user.id}")
        await message.reply("Secret key has been removed.")
    else:
        await message.reply("No secret key was set.")

@app.on_message(filters.command("viewsk", prefixes=["/", ".", "!"]))
async def view_sk(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to view the secret key.")
        return
    sk, pk, mt = await check_keys()
    
    if not sk:
        await message.reply("No secret key has been set.")
        return

    result_text = await check_status(message, sk, message.from_user.id)
    await message.reply(result_text)
