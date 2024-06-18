import os
import re
import asyncio
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import UserAlreadyParticipant
from EQUROBOT import app, scr

scrqtask = asyncio.Queue()

def rmv(mainsc):
    un = list(set(mainsc))
    dr = len(mainsc) - len(un)
    return un, dr

async def scrape(scr, chen, lim, bin=None):
    cmb = []
    pattern = r'\d{15,16}\D*\d{2}\D*\d{2,4}\D*\d{3,4}'

    async for message in scr.get_chat_history(chen, limit=lim):
        ccr = message.text if message.text else message.caption
        if ccr:
            scrm = re.findall(pattern, ccr)
            if scrm:
                fscrm = []
                for scrmn in scrm:
                    exv = re.findall(r'\d+', scrmn)
                    if len(exv) == 4:
                        cc, mes, ano, cvv = exv
                        ano = ano[-2:]
                        fscrm.append(f"{cc}|{mes}|{ano}|{cvv}")
                cmb.extend(fscrm)

    if bin:
        cmb = [cmbs for cmbs in cmb if cmbs.startswith(bin)]

    return cmb

@app.on_message(filters.command("scr", prefixes=[".", "/"]))
async def scr_oni(_, message: Message):
    message_cmd = message.text.split()

    if len(message_cmd) < 3:
        await message.reply("Wrong format. Usage: /scr <channel_url> <limit> [bin]", parse_mode=ParseMode.HTML)
        return

    chen = message_cmd[1]
    lim = int(message_cmd[2])

    if lim > 10000:
        await message.reply("Maximum limit is 10000.", parse_mode=ParseMode.HTML)
        return
    
    bin = message_cmd[3] if len(message_cmd) == 4 else None

    parsed_url = urlparse(chen)

    if parsed_url.scheme and parsed_url.netloc:
        if parsed_url.path.startswith('/+'):
            try:
                chat = await scr.join_chat(chen)
                chen = chat.id
            except UserAlreadyParticipant:
                try:
                    chat = await scr.get_chat(chen)
                    chen = chat.id
                except Exception as e:
                    await message.reply("Channel not found.", parse_mode=ParseMode.HTML)
                    return
            except Exception as e:
                await message.reply("Channel not found.", parse_mode=ParseMode.HTML)
                return
        else:
            chen = parsed_url.path.lstrip('/')
    else:
        chen = chen

    try:
        await scr.get_chat(chen)
    except Exception:
        await message.reply("Invalid channel or group.", parse_mode=ParseMode.HTML)
        return

    tempy = await message.reply("Scraping...", parse_mode=ParseMode.HTML)

    await scrqtask.put((message, chen, lim, bin, tempy))

async def pr_scrqtask(scr, bot):
    while True:
        task = await scrqtask.get()
        message, chen, lim, bin, tempy = task

        mainsc = await scrape(scr, chen, lim, bin)

        if mainsc:
            un, dr = rmv(mainsc)
            if un:
                file_name = f"{chen}x{len(un)}.txt"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write("\n".join(un))
                with open(file_name, 'rb') as f:
                    caption = (
                        f"CC Scrape Successful ✅\n\n"
                        f"[ϟ] Amount: <code>{len(un)}</code>\n"
                        f"[ϟ] Duplicate: <code>{dr}</code>\n"
                        f"[ϟ] Source: @{chen}\n\n"
                        f"[ϟ] Scraped By: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
                    )
                    await tempy.delete()
                    await bot.send_document(message.chat.id, f, caption=caption, parse_mode=ParseMode.HTML)
                os.remove(file_name)
            else:
                await tempy.delete()
                await message.reply("No credit card found.", parse_mode=ParseMode.HTML)
        else:
            await tempy.delete()
            await message.reply("No credit card found.", parse_mode=ParseMode.HTML)
        
        scrqtask.task_done()
