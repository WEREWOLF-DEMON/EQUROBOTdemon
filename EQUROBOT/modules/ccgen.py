import random
import logging
import aiohttp
import time
import re
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from EQUROBOT import app

async def get_bin_info(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    return (
                        bin_info.get("brand", "N/A"),
                        bin_info.get("type", "N/A"),
                        bin_info.get("level", "N/A"),
                        bin_info.get("bank", "N/A"),
                        bin_info.get("country_name", "N/A"),
                        bin_info.get("country_flag", "")
                    )
                except Exception:
                    return "Error parsing BIN info", "N/A", "N/A", "N/A", "N/A", "N/A"
            else:
                return "Error fetching BIN info", "N/A", "N/A", "N/A", "N/A", "N/A"

def luhn_algorithm(number):
    total_sum = 0
    reverse_digits = str(number)[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total_sum += n
    
    return total_sum % 10 == 0

def clean_card_details(card_details):
    card_details = re.sub(r'[xX]+', '0', card_details)
    card_details = card_details.replace('/', '|')
    return card_details

def generate_cvv(bin_part, provided_cvv):
    if provided_cvv.isdigit() and len(provided_cvv) in [3, 4]:
        return provided_cvv
    if bin_part.startswith("3"):
        return str(random.randint(1000, 9999))
    else:
        return str(random.randint(100, 999))

def generate_card_number(bin_part, remaining_length):
    while True:
        ccrem = "".join(random.choices("0123456789", k=remaining_length))
        ccgen = f"{bin_part}{ccrem}"
        
        if luhn_algorithm(ccgen):
            return ccgen

@app.on_message(filters.command(["gen"], [".", "!", "/"]))
async def generate_card(client, message):
    try:
        progress_message = await message.reply("**Generating Cards, please wait...**")
        tic = time.time()

        args = message.text.split()
        if len(args) < 2:
            await progress_message.edit("**Please provide a BIN to generate Cards.**")
            return

        card_details = clean_card_details(args[1])
        amount = int(args[2]) if len(args) > 2 and args[2].isdigit() else 10
        card_parts = card_details.split("|")

        full_bin = card_parts[0].strip()
        month = card_parts[1].strip() if len(card_parts) > 1 else ''
        year = card_parts[2].strip() if len(card_parts) > 2 else ''
        cvv = card_parts[3].strip() if len(card_parts) > 3 else ''
        
        if len(full_bin) < 6:
            full_bin = full_bin.ljust(6, '0')

        if len(full_bin) < 6:
            await progress_message.edit("**Please provide a valid 6-digit BIN.**")
            return

        bin_part = full_bin[:6]
        remaining_bin = full_bin[6:]
        card_length = 15 if bin_part.startswith("3") else 16
        remaining_length = card_length - len(bin_part) - len(remaining_bin)

        cards = []
        generated_months = set()

        for _ in range(amount):
            if month.isdigit() and 1 <= int(month) <= 12:
                monthdigit = month.zfill(2)
            else:
                monthdigit = str(random.randint(1, 12)).zfill(2)
                while monthdigit in generated_months:
                    monthdigit = str(random.randint(1, 12)).zfill(2)
                generated_months.add(monthdigit)

            if year.isdigit() and (len(year) == 2 or len(year) == 4):
                if len(year) == 2:
                    yeardigit = f"20{year}"
                else:
                    yeardigit = year
            else:
                yeardigit = str(random.randint(2024, 2032))

            ccgen = generate_card_number(full_bin, remaining_length)
            cvvdigit = generate_cvv(bin_part, cvv)
            cards.append(f"{ccgen}|{monthdigit}|{yeardigit}|{cvvdigit}")

        user = message.from_user
        profile_link = f"https://t.me/{user.username}"
        fullname = user.first_name + (" " + user.last_name if user.last_name else "")
        
        brand, card_type, level, bank, country, country_flag = await get_bin_info(bin_part)
        toc = time.time()

        await progress_message.delete()

        if amount > 10:
            file_name = "cards.txt"
            with open(file_name, "w") as file:
                file.write("\n".join(cards))
            
            caption = (
                f"**BIN** ⇾ `{bin_part}`\n"
                f"**Amount** ⇾ `{amount}`\n"
                f"**Info** ⇾ `{brand}` - `{card_type}` - `{level}`\n"
                f"**Issuer** ⇾ `{bank}`\n"
                f"**Country** ⇾ `{country}` {country_flag}\n"
                f"**Time Taken** ⇾ {toc - tic:.2f} seconds\n"
                f"**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ** ‌: [{fullname}]({profile_link})"
            )
            
            await client.send_document(
                chat_id=message.chat.id,
                document=file_name,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN,
                reply_to_message_id=message.id
            )
        else:
            card_response = "\n".join([f"`{card}`" for card in cards])
            
            response = (
                f"**BIN** ⇾ `{bin_part}`\n"
                f"**Amount** ⇾ `{amount}`\n"
                f"{card_response}\n\n"
                f"**Info** ⇾ `{brand}` - `{card_type}` - `{level}`\n"
                f"**Issuer** ⇾ `{bank}`\n"
                f"**Country** ⇾ `{country}` {country_flag}\n"
                f"**Time Taken** ⇾ {toc - tic:.2f} seconds\n"
                f"**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ** ‌: [{fullname}]({profile_link})"
            )

            await message.reply(
                response,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )

    except Exception as e:
        logging.error(e)
        await message.reply(
            f"Error: {str(e)}\nMake sure your input format is: /gen 44542300072|xx|xxxx|xxx 10"
        )
        
