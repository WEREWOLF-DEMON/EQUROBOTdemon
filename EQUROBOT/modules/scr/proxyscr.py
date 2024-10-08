import re
import asyncio
import time
from pyrogram import filters
from pyrogram.types import Message
from os import remove as osremove
from urllib.parse import urlparse
from EQUROBOT import app
from EQUROBOT import scr as userbot


def extract_proxy_details(text):
    pattern = r'(\d{1,3}(?:\.\d{1,3}){3}):(\d{2,5}):(\w+):(\w+)'
    proxies = re.findall(pattern, text)
    
    formatted_proxies = [f"{ip}:{port}:{username}:{password}" for ip, port, username, password in proxies]
    
    return formatted_proxies

async def join_channel_with_approval(userbot, channel_url):
    while True:
        try:
            return await userbot.join_chat(channel_url)
        except Exception as e:
            error_message = str(e)
            if 'This is a private channel and you need to join it first' in error_message:
                await asyncio.sleep(5)
            elif 'The invite link is invalid or has expired' in error_message:
                raise ValueError("Invalid or expired invite link.")
            elif 'USER_ALREADY_PARTICIPANT' in error_message:
                return await userbot.get_chat(channel_url)
            else:
                raise e

async def animate_processing(message):
    animation_frames = ['■□□□', '■■□□', '■■■□', '■■■■']
    processing_msg = await message.reply("Processing your request\nPlease wait")
    try:
        while True:
            for frame in animation_frames:
                await processing_msg.edit_text(f"Processing your request\nPlease wait {frame}")
                await asyncio.sleep(3.5)
    except asyncio.CancelledError:
        await processing_msg.delete()

@app.on_message(filters.command("proxyscr", prefixes=[".", "/"]))
async def scr_oni(_, message: Message):
    args = message.text.split(' ')[1:]

    if len(args) < 2:
        resp = """
**Wrong Format ❌**

**Usage:**
**For Public Group/Channel Scraping**
`/proxyscr [username] [Amount]`

**For Private Group/Channel Scraping**
`/proxyscr [link] [Amount]`
        """
        await message.reply_text(resp)
        return

    channel_url = args[0]
    limit = int(args[1]) if args[1].isdigit() else 100
    bin = args[2] if len(args) > 2 else None

    parsed_url = urlparse(channel_url)

    if parsed_url.scheme and parsed_url.netloc and parsed_url.path.startswith('/+'):
        try:
            chat_info = await join_channel_with_approval(userbot, channel_url)
            channel_id = chat_info.id
        except Exception as e:
            await message.reply(f"Error joining channel: {str(e)}")
            return
    else:
        channel_id = parsed_url.path.lstrip('/') if parsed_url.scheme else channel_url

    processing_task = asyncio.create_task(animate_processing(message))

    tic = time.time()

    try:
        mainsc = await scrape(userbot, channel_id, limit, bin)
    except Exception as e:
        processing_task.cancel()
        await processing_task
        await message.reply(f"Error scraping: {str(e)}")
        return

    toc = time.time()
    processing_task.cancel()
    await processing_task

    if mainsc:
        unique_proxies, duplicates_removed = rmv(mainsc)
        if unique_proxies:
            file_name = f"EQU_X_{channel_id}_X_{len(unique_proxies)}_proxies.txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write("\n".join(unique_proxies))

            with open(file_name, 'rb') as f:
                caption = (
                    f"**𝗣𝗿𝗼𝘅𝘆 𝗦𝗰𝗿𝗮𝗽𝗽𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅**\n\n"
                    f"❁ **Amount** ➜ `{len(unique_proxies)}`\n"
                    f"❁ **Duplicate** ➜ `{duplicates_removed}`\n"
                    f"❁ **Source** ➜ {channel_id}\n"
                    f"❁ **Time Taken** ➜ {toc - tic:.2f} seconds\n\n"
                    f"❁ **Scraped By** ➜ [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                )
                await app.send_document(message.chat.id, f, caption=caption)
            osremove(file_name)
        else:
            await message.reply("No proxies found.")
    else:
        await message.reply("No proxies found.")

async def scrape(userbot, channel_id, limit, bin=None):
    proxies = []
    async for message in userbot.get_chat_history(channel_id, limit=limit):
        content = message.text if message.text else message.caption
        if content:
            found_proxies = extract_proxy_details(content)
            if found_proxies:
                proxies.extend(found_proxies)

    if bin:
        proxies = [proxy for proxy in proxies if proxy.startswith(bin)]

    return proxies

def rmv(proxy_list):
    unique_proxies = list(set(proxy_list))
    duplicates_removed = len(proxy_list) - len(unique_proxies)
    return unique_proxies, duplicates_removed
