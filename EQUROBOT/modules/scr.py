import asyncio
from pathlib import Path
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from urllib.parse import urlparse
from EQUROBOT import app, scr


def getcards(text: str, bin_number=None):
    text = text.replace('\n', ' ').replace('\r', '')
    card = re.findall(r"[0-9]+", text)
    if not card or len(card) < 4:
        return None

    cc, mes, ano, cvv = card[:4]
    if len(mes) != 2 or not ('01' <= mes <= '12'):
        mes, ano = ano, mes

    if not (cc.startswith(('3', '4', '5', '6')) and (len(cc) in [15, 16])):
        return None
    if len(mes) != 2 or not ('01' <= mes <= '12'):
        return None
    if len(ano) not in [2, 4] or (len(ano) == 2 and not ('21' <= ano <= '39')) or (len(ano) == 4 and not ('2021' <= ano <= '2039')):
        return None
    if cc.startswith('3') and len(cvv) != 4 or len(cvv) != 3:
        return None

    if bin_number and not cc.startswith(bin_number):
        return None
    
    return cc, mes, ano, cvv


@app.on_message(filters.command('scr'))
async def cmd_scr(client, message):
    msg = message.text[len('/scr '):].strip()
    splitter = msg.split(' ')
    
    if not msg or len(splitter) < 2:
        resp = """
𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁 ❌

𝗨𝘀𝗮𝗴𝗲:
𝗙𝗼𝗿 𝗣𝘂𝗯𝗹𝗶𝗰 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr username amount [bin_number]</code>

𝗙𝗼𝗿 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr https://t.me/+aGWRGz amount [bin_number]</code>
        """
        await message.reply_text(resp, message.id)
        return

    try:
        limit = int(splitter[1])
    except ValueError:
        limit = 100

    bin_number = splitter[2] if len(splitter) > 2 else None

    delete = await message.reply_text("𝗦𝗰𝗿𝗮𝗽𝗶𝗻𝗴 𝗪𝗮𝗶𝘁...", message.id)
    channel_link = splitter[0]
    
    async def scrape_channel(channel_id, limit, title, bin_number=None):
        amt_cc = 0
        duplicate = 0
        file_name = f"{limit}x_CC_Scraped_By_@YesikooBot.txt"

        with open(file_name, 'w') as f:
            pass  # Create the file

        async for msg in scr.get_chat_history(channel_id, limit):
            all_history = msg.text or ""
            all_cards = all_history.split('\n')
            cards = [getcards(x, bin_number) for x in all_cards if getcards(x, bin_number)]
            
            if not cards:
                continue
            
            for item in cards:
                amt_cc += 1
                cc, mes, ano, cvv = item
                fullcc = f"{cc}|{mes}|{ano}|{cvv}"
                
                with open(file_name, 'a') as f:
                    cclist = open(file_name).read().splitlines()
                    if fullcc in cclist:
                        duplicate += 1
                    else:
                        f.write(f"{fullcc}\n")

        total_cc = amt_cc
        cc_found = total_cc - duplicate
        await app.delete_messages(message.chat.id, delete.id)
        caption = f"""
𝗖𝗖 𝗦𝗰𝗿𝗮𝗽𝗲𝗱 ✅

● 𝗦𝗼𝘂𝗿𝗰𝗲: {title}
● 𝗧𝗮𝗿𝗴𝗲𝘁𝗲𝗱 𝗔𝗺𝗼𝘂𝗻𝘁: {limit}
● 𝗖𝗖 𝗙𝗼𝘂𝗻𝗱: {cc_found}
● 𝗗𝘂𝗽𝗹𝗶𝗰𝗮𝘁𝗲 𝗥𝗲𝗺𝗼𝘃𝗲𝗱: {duplicate}
● 𝗦𝗰𝗿𝗮𝗽𝗲𝗱 𝗕𝘆: <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a> ♻️
"""
        if cc_found > 0:
            scr_done = await app.send_document(
                message.chat.id,
                document=file_name,
                caption=caption,
                reply_to_message_id=message.id
            )

            if scr_done:
                Path(file_name).unlink(missing_ok=True)
        else:
            await message.reply_text("No valid CCs found to write to the file.", message.id)

    try:
        if "https" in channel_link:
            join = await scr.join_chat(channel_link)
            await scrape_channel(join.id, limit, join.title, bin_number)
        else:
            chat_info = await scr.get_chat(channel_link)
            await scrape_channel(chat_info.id, limit, chat_info.title, bin_number)
    except Exception as e:
        error_message = str(e)
        if '[400 USER_ALREADY_PARTICIPANT]' in error_message:
            chat_info = await scr.get_chat(channel_link)
            await scrape_channel(chat_info.id, limit, chat_info.title, bin_number)
        elif '[400 USERNAME_INVALID]' in error_message:
            resp = """
𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁 ❌

𝗨𝘀𝗮𝗴𝗲:
𝗙𝗼𝗿 𝗣𝘂𝗯𝗹𝗶𝗰 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr username amount [bin_number]</code>

𝗙𝗼𝗿 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr https://t.me/+aGWRGz amount [bin_number]</code>
        """
            await message.reply_text(resp, message.id)
            await delete.delete()
        elif '[400 INVITE_HASH_EXPIRED]' in error_message:
            await message.reply_text("The invite link is expired. Please provide a valid link.", message.id)
            await delete.delete()
        else:
            await message.reply_text(f"An error occurred: {error_message}", message.id)
            await delete.delete()
