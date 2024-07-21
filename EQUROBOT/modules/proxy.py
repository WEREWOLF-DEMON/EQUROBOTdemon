from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from EQUROBOT import app


def check_proxy(proxy):
    url = "https://httpbin.org/ip"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"https://{proxy}",
    }
    
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return "Live ✅"
        else:
            return "Dead ❌"
    except requests.RequestException:
        return "Dead ❌"


@app.on_message(filters.command("proxy"))
async def single_proxy_handler(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: /proxy <single_proxy>")
        return
    
    proxy = message.command[1]
    result = check_proxy(proxy)
    response = f"""
┏━━━━━━━⍟
┃𝗣𝗿𝗼𝘅𝘆 𝗖𝗵𝗲𝗰𝗸𝗲𝗿
┗━━━━━━━━━━━⊛

{proxy}
𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {result}

⌥ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: {message.from_user.first_name}
"""
    await message.reply(response)


@app.on_message(filters.command("mproxy"))
async def multiple_proxy_handler(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: /mproxy <max_number_of_proxies>")
        return
    
    try:
        max_proxies = int(message.command[1])
        if max_proxies > 25:
            await message.reply("Maximum allowed proxies to check at a time is 25.")
            return
    except ValueError:
        await message.reply("Please provide a valid number.")
        return
    
    await message.reply("Please send the proxies, one per line.")
    
    proxies_to_check = []

    @app.on_message(filters.text & filters.reply)
    async def reply_handler(client: Client, msg: Message):
        if msg.reply_to_message and msg.reply_to_message.from_user.id == client.me.id:
            proxies = msg.text.strip().split("\n")
            for proxy in proxies[:max_proxies]:
                result = check_proxy(proxy)
                response = f"""
┏━━━━━━━⍟
┃𝗣𝗿𝗼𝘅𝘆 𝗖𝗵𝗲𝗰𝗸𝗲𝗿
┗━━━━━━━━━━━⊛

{proxy}
𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {result}

⌥ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆: {msg.from_user.first_name}
"""
                proxies_to_check.append(response)
            await msg.reply("\n".join(proxies_to_check))
