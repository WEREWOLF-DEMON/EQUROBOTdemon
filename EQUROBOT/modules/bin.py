import requests
from pyrogram import Client, filters
from EQUROBOT import app


@app.on_message(filters.command("bin"))
async def bin_lookup(client, message):
    bin_number = message.text.split(" ")[1]
    
    headers = {
        'Accept-Version': '3',
    }

    r = requests.get(f'https://lookup.binlist.net/{bin_number}', headers=headers)
    data = r.json()

    bin_info = f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍

𝗕𝗜𝗡 ⇾ `{bin_number}`

𝗜𝗻𝗳𝗼 ⇾ `{data.get('scheme', 'N/A').upper()} - {data.get('type', 'N/A').upper()} - {data.get('brand', 'N/A').upper()}`
𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ `{data.get('bank', {}).get('name', 'N/A').upper()}`
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ `{data.get('country', {}).get('name', 'N/A').upper()} {data.get('country', {}).get('emoji', '')}`
"""

    await message.reply_text(bin_info)
