import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from os import remove as osremove
from urllib.parse import urlparse
from EQUROBOT import app, scr

def extract_cc_details(text):
    pattern = r'\d{15,16}\D*\d{2}\D*\d{2,4}\D*\d{3,4}'
    cc_details = re.findall(pattern, text)
    valid_cc = []
    for cc in cc_details:
        exv = re.findall(r'\d+', cc)
        if len(exv) == 4:
            cc, mes, ano, cvv = exv
            ano = ano[-2:]
            valid_cc.append(f"{cc}|{mes}|{ano}|{cvv}")
    return valid_cc

@app.on_message(filters.command("scr", prefixes=[".", "/"]))
async def scr_oni(_, message: Message):
    msg = message.text[len('/scr '):].strip()
    splitter = msg.split(' ')
    
    if not msg or len(splitter) < 2:
        resp = """
𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁 ❌

𝗨𝘀𝗮𝗴𝗲:
𝗙𝗼𝗿 𝗣𝘂𝗯𝗹𝗶𝗰 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr username 50</code>

𝗙𝗼𝗿 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr https://t.me/+aGWRGz 50</code>
        """
        await message.reply_text(resp, message.id)
        return

    try:
        limit = int(splitter[1])
    except ValueError:
        limit = 100

    channel_url = splitter[0]
    if len(splitter) < 3:
        bin = splitter[2]
    parsed_url = urlparse(channel_url)

    if parsed_url.scheme and parsed_url.netloc:
        if parsed_url.path.startswith('/+'):
            try:
                chat = await scr.join_chat(channel_url)
                channel_id = chat.id
            except Exception as e:
                return await message.reply("Channel not found.", parse_mode=ParseMode.HTML)
        else:
            channel_id = parsed_url.path.lstrip('/')
    else:
        channel_id = channel_url

    try:
        await scr.get_chat(channel_id)
    except Exception:
        return await message.reply("Invalid channel or group.", parse_mode=ParseMode.HTML)

    temp_message = await message.reply_text("𝗦𝗰𝗿𝗮𝗽𝗶𝗻𝗴 𝗪𝗮𝗶𝘁...", message.id)
    try:
        mainsc = await scrape(scr, channel_id, limit, bin)
    except Exception as e:
        return await message.reply(f"Error scraping: {str(e)}", parse_mode=ParseMode.HTML)

    if mainsc:
        un, dr = rmv(mainsc)
        if un:
            file_name = f"{channel_id}x{len(un)}.txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write("\n".join(un))

            with open(file_name, 'rb') as f:
                caption = (
                    f"CC Scrape Successful ✅\n\n"
                    f"[ϟ] Amount: <code>{len(un)}</code>\n"
                    f"[ϟ] Duplicate: <code>{dr}</code>\n"
                    f"[ϟ] Source: @{channel_id}\n\n"
                    f"[ϟ] Scraped By: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
                )
                await temp_message.delete()
                await app.send_document(message.chat.id, f, caption=caption, parse_mode=ParseMode.HTML)
            osremove(file_name)
        else:
            await temp_message.delete()
            await message.reply("No credit card found.", parse_mode=ParseMode.HTML)
    else:
        await temp_message.delete()
        await message.reply("No credit card found.", parse_mode=ParseMode.HTML)

async def scrape(scr, channel_id, limit, bin=None):
    cmb = []
    async for message in scr.get_chat_history(channel_id, limit=limit):
        ccr = message.text if message.text else message.caption
        if ccr:
            valid_cc = extract_cc_details(ccr)
            if valid_cc:
                cmb.extend(valid_cc)

    if bin:
        cmb = [cc for cc in cmb if cc.startswith(bin)]

    return cmb

def rmv(cc_list):
    unique_cc = list(set(cc_list))
    duplicates_removed = len(cc_list) - len(unique_cc)
    return unique_cc, duplicates_removed
