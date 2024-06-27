import re
import time
from pyrogram import Client, filters, types
from pyrogram.enums import ParseMode
from os import remove as osremove
from EQUROBOT import app, scr

def extract_sk_live_details(string):
    sk_lives = re.findall(r'sk_live_[a-zA-Z0-9]+', string)
    return sk_lives

@app.on_message(filters.command(["skscr", "scrsk"], prefixes=[".", "/"]))
async def skscr_command(_, message):
    user_id = message.from_user.id
    limit = 5000
    try:
        command, channel_url, amount = message.text.split()
        amount = int(amount)
        if amount > limit:
            return await message.reply(f"𝗟𝗜𝗠𝗜𝗧 𝗧𝗢 𝗦𝗖𝗥𝗔𝗣𝗘 {limit} ⚠️")
    except ValueError:
        return await message.reply("𝗪𝗥𝗢𝗡𝗚 𝗙𝗢𝗥𝗠𝗔𝗧 ⚠️", parse_mode=ParseMode.HTML)

    try:
        entity = await scr.get_chat(channel_url)
    except:
        entity = None
    if not entity:
        return await message.reply("𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘 ⚠️", parse_mode=ParseMode.HTML)

    Tempmess = await message.reply("𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴 𝘀𝗸...", parse_mode=ParseMode.HTML)
    results = []

    async for event in scr.get_chat_history(chat_id=entity.id, limit=amount):
        if event.text:
            sk_lives = extract_sk_live_details(event.text)
            results.extend(sk_lives)
        elif event.caption:
            sk_lives = extract_sk_live_details(event.caption)
            results.extend(sk_lives)

    if results:
        file_name = f"{entity.username if entity.username else 'chat'}_sk_{len(results)}.txt"
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
            await message.reply_document(file_name, caption=caption, parse_mode=ParseMode.HTML)
        except Exception as e:
            await message.reply(f"𝗘𝗿𝗿𝗼𝗿: {str(e)}", parse_mode=ParseMode.HTML)
        finally:
            osremove(file_name)
    else:
        await Tempmess.delete()
        await message.reply("𝗡𝗼 𝗦𝗞 𝗙𝗼𝘂𝗻𝗱", parse_mode=ParseMode.HTML)

