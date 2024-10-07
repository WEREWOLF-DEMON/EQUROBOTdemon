import asyncio
import aiohttp
import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from EQUROBOT.core.mongo import has_premium_access
from EQUROBOT import app
from config import OWNER_ID

async def check_proxy(proxy):
    url = "http://httpbin.org/ip"
    try:
        proxy_parts = proxy.split(":")
        proxy_auth = aiohttp.BasicAuth(*proxy_parts[2:]) if len(proxy_parts) == 4 else None
        proxy_url = f"http://{proxy_parts[0]}:{proxy_parts[1]}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy_url, proxy_auth=proxy_auth, timeout=5) as response:
                return proxy, "**Live** ✅" if response.status == 200 else "**Dead** ❌"
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logging.error(f"Error checking proxy {proxy}: {e}")
        return proxy, "Dead ❌"

async def animate_processing(message, total_proxies=None, progress=None):
    animation_frames = ['■□□□', '■■□□', '■■■□', '■■■■']
    processing_msg = await message.reply("Processing your request...")
    try:
        while True:
            for frame in animation_frames:
                if total_proxies is not None and progress is not None:
                    await processing_msg.edit_text(
                        f"Checking {total_proxies} Proxies\n"
                        f"Checked: {progress['count']}/{total_proxies} {frame}"
                    )
                else:
                    await processing_msg.edit_text(f"Processing... {frame}")
                await asyncio.sleep(3.5)
    except asyncio.CancelledError:
        await processing_msg.delete()

def extract_proxies(text):
    return [line.strip() for line in text.splitlines() if ":" in line.strip()]

def extract_proxies_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if ":" in line.strip()]

def save_live_proxies(checked_proxies):
    live_proxies_path = "Flash_X_Live_Proxies.txt"
    live_proxies = [proxy for proxy, status in checked_proxies if "Live" in status]
    
    if live_proxies:
        with open(live_proxies_path, 'w') as f:
            f.write("\n".join(live_proxies))
        return live_proxies_path
    return None

@app.on_message(filters.command(["proxytxt"], [".", "/"]))
async def check_proxies_handler(client: Client, message: Message):

    if not await has_premium_access(message.from_user.id) and message.from_user.id != OWNER_ID:
        return await message.reply_text("You don't have premium access. Contact my owner to purchase premium.")
        
    if not message.reply_to_message:
        await message.reply_text("Please reply to a message containing proxy addresses or a document to check.")
        return
    
    if message.reply_to_message.document:
        file_path = await message.reply_to_message.download()
        proxies_list = extract_proxies_from_file(file_path)
        os.remove(file_path)
    else:
        proxy_text = message.reply_to_message.text
        proxies_list = extract_proxies(proxy_text)

    if not proxies_list:
        await message.reply_text("No valid proxies found.")
        return

    total_proxies = len(proxies_list)
    progress = {'count': 0}
    
    processing_task = asyncio.create_task(animate_processing(message, total_proxies, progress))

    checked_proxies = []
    for proxy in proxies_list:
        status = await check_proxy(proxy)
        checked_proxies.append(status)
        progress['count'] += 1
    
    processing_task.cancel()
    await processing_task

    live_proxies_file = save_live_proxies(checked_proxies)
    
    if live_proxies_file:
        await message.reply_document(live_proxies_file)
        os.remove(live_proxies_file)
    else:
        await message.reply_text("__No Live Proxies found.__")
