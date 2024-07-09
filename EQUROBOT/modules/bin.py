import httpx
from pyrogram import Client, filters
from EQUROBOT import app

import aiohttp
from pyrogram import Client, filters, enums

#

import aiohttp
from pyrogram import Client, filters, enums

# Assuming you have defined `app` elsewhere in your code as the Pyrogram Client instance

# Function to fetch BIN information
async def bin_lookup(bin_number):
    astroboyapi = f"https://daxxteam.com/binapi?bins={bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(astroboyapi) as response:
            if response.status == 200:
                try:
                    if response.headers['content-type'] == 'application/json':
                        bin_info = await response.json()
                        brand = bin_info.get("brand", "N/A")
                        card_type = bin_info.get("type", "N/A")
                        level = bin_info.get("level", "N/A")
                        bank = bin_info.get("bank", "N/A")
                        country = bin_info.get("country_name", "N/A")
                        country_flag = bin_info.get("country_flag", "")
                        
                        bin_info_text = f"""
┏━━━━━━━⍟
┃𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍
┗━━━━━━━━━━━⊛

[ϟ] 𝗕𝗶𝗻: <code>{bin_number}</code>
[ϟ] 𝗜𝗻𝗳𝗼: {brand} - {card_type} - {level}
[ϟ] 𝗕𝗮𝗻𝗸: {bank}
[ϟ] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} {country_flag}
"""
                        return bin_info_text
                    else:
                        return f"Error: Unexpected API response format ({response.headers['content-type']})"
                except Exception as e:
                    return f"Error: Failed to parse JSON ({str(e)})"
            else:
                return f"Error: Unable to retrieve BIN information (Status code: {response.status})"

# Command to handle BIN lookup
@app.on_message(filters.command("bin", prefixes="."))
async def bin_command(client, message):
    if len(message.text.split()) >= 2:
        bin_number = message.text.split()[1]
        bin_number = bin_number[:6]  # Extract first 6 digits of the BIN
    elif message.reply_to_message and message.reply_to_message.text:
        bin_number = message.reply_to_message.text[:6]  # Extract BIN from replied message
    else:
        await message.reply("Provide a valid BIN to check", parse_mode=enums.ParseMode.HTML)
        return
    
    bin_info = await bin_lookup(bin_number)
    user_id = message.from_user.id

    await message.reply(f'''
{bin_info}

[ϟ] Checked By ➺ <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>
''', parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    
