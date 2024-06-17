import re
import time
from aiogram import types
from os import remove as osremove
from EQUROBOT import app
from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram import *
#app = Client("my_app", api_id=12345, api_hash="my_api_hash", bot_token="my_bot_token")

def extract_sk_live_details(string):
    sk_lives = re.findall(r'sk_live_[a-zA-Z0-9]+', string)
    return sk_lives

@app.on_message(filters.command("scrsk"))
async def scr_sk(client, message):
    user_id = message.from_user.id
    limit = 500
    try:
        command, channel_url, amount = message.text.split()
        amount = int(amount)
        amount = min(amount, limit + 1)
        if amount > limit:
            return await message.reply(f"𝗟𝗜𝗠𝗜𝗧 𝗧𝗢 𝗦𝗖𝗥𝗔𝗣𝗘 {limit} ⚠️")
    except ValueError:
        return await message.reply("𝗪𝗥𝗢𝗡𝗚 𝗙𝗢𝗥𝗠𝗔𝗧 ⚠️", parse_mode='HTML')

    #user_client = Client("user_client", api_id=12345, api_hash="my_api_hash")
    await app.start()

    try:
        entity = await app.get_chat(channel_url)
    except:
        entity = None
    if not entity:
        return await message.reply("𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘 ⚠️", parse_mode='HTML')

    Tempmess = await message.reply("𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴 𝘀𝗸...", parse_mode='HTML')
    results = []

    async for event in app.get_chat_history(chat_id=entity.id, limit=amount):
        if event.text:
            sk_lives = extract_sk_live_details(str(event.text))
            results.extend(sk_lives)
        elif event.caption:
            sk_lives = extract_sk_live_details(str(event.caption))
            results.extend(sk_lives)

    if results:
        file_name = f"{entity.username if entity.username else ''}x{len(results)}.txt"
        with open(file_name, 'w') as file:
            for sk_live in results:
                file.write(sk_live + '\n')

        caption = f"""
𝗦𝗞 𝗦𝗖𝗥𝗔𝗣𝗣𝗘𝗗 ✅

[ϟ] 𝗔𝗺𝗼𝘂𝗻𝘁 : <code>{amount}</code>
[ϟ] 𝗦𝗞 𝗙𝗼𝘂𝗻𝗱 : <code>{len(results)}</code>
[ϟ] 𝗦𝗼𝘂𝗿𝗰𝗲 : @{entity.username}

[ϟ] 𝗦𝗰𝗿𝗮𝗽𝗽𝗲𝗱 𝗕𝘆 : <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
"""
        try:
            await Tempmess.delete()
            await message.reply_document(types.InputFile(file_name), caption=caption, parse_mode='HTML')
        except BadRequest:
            await Tempmess.delete()
            await message.answer_document(types.InputFile(file_name), caption=caption, parse_mode='HTML')
        osremove(file_name)
    else:
        await Tempmess.delete()
        await message.reply("𝗡𝗼 𝗦𝗞 𝗙𝗼𝘂𝗻𝗱", parse_mode='HTML')
