import aiohttp
from pyrogram import Client, filters, enums
from EQUROBOT import app

async def bin_lookup(bin_number):
    antipublic_url = f"https://bins.antipublic.cc/bins/{bin_number}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(antipublic_url) as response:
                if response.status == 200:
                    try:
                        bin_info = await response.json()
                        if not bin_info or "error" in bin_info:
                            return "🚫 BIN not recognized. Please enter a valid BIN."

                        brand = bin_info.get("brand", "--")
                        card_type = bin_info.get("type", "--")
                        level = bin_info.get("level", "--")
                        bank = bin_info.get("bank", "--")
                        country = bin_info.get("country_name", "--")
                        country_flag = bin_info.get("country_flag", "--")

                        bin_info_text = f"""
𝗕𝗜𝗡 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍

𝗕𝗜𝗡 ⇾ <code>{bin_number}</code>
𝗜𝗻𝗳𝗼 ⇾ {brand} - {card_type} - {level}
𝐈𝐬𝐬𝐮𝐞𝐫 ⇾ {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ⇾ {country} {country_flag}
"""
                        return bin_info_text
                    except Exception as e:
                        return f"Error: Unable to retrieve BIN information ({str(e)})"
                else:
                    return f"Error: Received a {response.status} status code from the server."

        except aiohttp.ClientError as e:
            return f"Error: Network or server issue ({str(e)})"

@app.on_message(filters.command("bin", prefixes=[".", "!", "/"]))
async def bin_command(client, message):
    bin_number = message.text.split(maxsplit=1)[-1].strip()
    if not bin_number or not bin_number.isdigit() or len(bin_number) < 6:
        await message.reply("🚫 Please provide a valid BIN number (at least 6 digits).")
        return

    response_text = await bin_lookup(bin_number)
    await message.reply(response_text, parse_mode=enums.ParseMode.HTML)
    
