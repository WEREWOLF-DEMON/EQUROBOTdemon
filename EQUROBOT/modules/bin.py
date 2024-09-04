import aiohttp
from pyrogram import Client, filters, enums
from EQUROBOT import app

# Function to fetch BIN information
async def bin_lookup(bin_number):
    antipublic_url = f"https://bins.antipublic.cc/bins/{bin_number}"

    async with aiohttp.ClientSession() as session:
        async with session.get(antipublic_url) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    if not bin_info or "error" in bin_info:
                        return "🚫 BIN not recognized. Please enter a valid BIN."

                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")
                    
                    bin_info_text = f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍

𝗕𝗜𝗡 ⇾ <code>{bin_number}</code>
𝗜𝗻𝗳𝗼 ⇾ {brand} - {card_type} - {level}
𝐈𝐬𝐬𝐵𝐨𝐛𝐨𝐧 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country} {country_flag}
"""
                    return bin_info_text
                except Exception as e:
                    return f"Error: Unable to retrieve BIN information ({str(e)})"
            else:
                return f"Error: Unable to retrieve BIN information (Status code: {response.status})"

# Command to handle BIN lookup
@app.on_message(filters.command("bin", prefixes="."))
async def bin_command(client, message):
    if len(message.text.split()) >= 2:
        bin_number = message.text.split()[1]
        if not (6 <= len(bin_number) <= 16) or not bin_number.isdigit():
            await message.reply("🚫 Incorrect input. Please provide a BIN number between 6 and 16 digits.", parse_mode=enums.ParseMode.HTML)
            return
    elif message.reply_to_message and message.reply_to_message.text:
        bin_number = message.reply_to_message.text.strip()[:16]  # Allow up to 16 digits
        if not (6 <= len(bin_number) <= 16) or not bin_number.isdigit():
            await message.reply("🚫 Incorrect input. Please provide a BIN number between 6 and 16 digits.", parse_mode=enums.ParseMode.HTML)
            return
    else:
        await message.reply("🚫 Incorrect input. Please provide a BIN number between 6 and 16 digits.", parse_mode=enums.ParseMode.HTML)
        return
    
    bin_info = await bin_lookup(bin_number)
    
    await message.reply(f'{bin_info}', parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    
