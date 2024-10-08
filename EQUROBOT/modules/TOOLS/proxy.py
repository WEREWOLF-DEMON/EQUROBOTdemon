import asyncio
import aiohttp
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
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
                return proxy, "Live ✅" if response.status == 200 else "Dead ❌"
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        return proxy, "Dead ❌"

@app.on_message(filters.command("proxy"))
async def single_proxy_handler(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: `/proxy ip:port:username:password`")
        return

    proxies = message.command[1:]
    user_id = message.from_user.id

    if user_id != OWNER_ID and len(proxies) > 25:
        await message.reply("You can check a maximum of 25 proxies at a time.")
        return

    tasks = [check_proxy(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)

    proxy_responses = "\n".join([f"`{proxy}`\nResponse ➜ **{result}**" for proxy, result in results])

    final_message = f"""
┏━━━━━━━⍟
┃𝗣𝗿𝗼𝘅𝘆 𝗖𝗵𝗲𝗰𝗸𝗲𝗿 ✅
┗━━━━━━━━━━━━━━⊛

{proxy_responses}

Checked by ➜ {message.from_user.mention}
"""
    await message.reply(final_message)
