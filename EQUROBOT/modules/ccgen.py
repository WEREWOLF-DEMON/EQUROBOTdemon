import re
from pyrogram import filters, enums
from EQUROBOT import app

import io
import random
import aiohttp

def checkLuhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')

        if isSecond:
            d = d * 2

        nSum += d // 10
        nSum += d % 10

        isSecond = not isSecond

    return nSum % 10 == 0

def cc_gen(cc, amount, mes='x', ano='x', cvv='x'):
    am = amount
    generated = 0
    ccs = []

    while generated < am:
        s = "0123456789"
        l = list(s)
        random.shuffle(l)
        result = ''.join(l)
        result = cc + result

        if cc[0] == "3":
            ccgen = result[:15]
        else:
            ccgen = result[:16]

        if checkLuhn(ccgen):
            generated += 1
        else:
            continue

        if mes == 'x':
            mesgen = random.randint(1, 12)
            if len(str(mesgen)) == 1:
                mesgen = "0" + str(mesgen)
        else:
            mesgen = mes

        if ano == 'x':
            anogen = random.randint(2024, 2032)
        else:
            anogen = ano

        if cvv == 'x':
            if cc[0] == "3":
                cvvgen = random.randint(1000, 9999)
            else:
                cvvgen = random.randint(100, 999)
        else:
            cvvgen = cvv

        lista = f"{ccgen}|{mesgen}|{anogen}|{cvvgen}"
        ccs.append(lista)

    return ccs

async def bin_lookup(bin_number):
    astroboyapi = f"https://astroboyapi.com/api/bin.php?bin={bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(astroboyapi) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")

                    bin_info_text = f"{brand} - {card_type} - {level}\n𝐈𝐬𝐬𝐮𝐞𝐫: {bank}\n𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} {country_flag}"
                    return bin_info_text
                except Exception as e:
                    return f"Error: Unable to retrieve BIN information ({str(e)})"
            else:
                return f"Error: Unable to retrieve BIN information (Status code: {response.status})"

async def generate_cc(client, message):
    if len(message.text.split()) == 2:
        text = message.text.split()[1]
        amount = int(10)
    elif len(message.text.split()) == 3:
        text = message.text.split()[1]
        amount = int(message.text.split()[2])
    else:
        await message.reply("Invalid input. Please provide a BIN (Bank Identification Number) that is at least 6 digits but not exceeding 16 digits.\n\nExample: .gen 412236xxxx|xx|2024|xxx", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
        return

    if amount > 30000:
        await message.reply("𝗟𝗜𝗠𝗜𝗧 𝗧𝗢 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘 30000 ⚠️", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
        return

    params = re.sub('x+', 'x', text).split('|')
    if len(params[0]) < 6:
        await message.reply("Invalid BIN.", disable_web_page_preview=True)
        return

    loading_message = await message.reply("𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗻𝗴 𝗰𝗰", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    cc = params[0].replace('x', '')
    expiration_month = int(params[1]) if len(params) > 1 and params[1] != 'x' else 'x'
    expiration_year = int(params[2]) if len(params) > 2 and params[2] != 'x' else 'x'
    cvv = params[3] if len(params) > 3 and params[3] != 'x' else 'x'

    ccs = cc_gen(cc, amount, expiration_month, expiration_year, cvv)
    astro = '\n'.join([f"{cc}" for cc in ccs])

    bin_info = await bin_lookup(cc[:6])

    mess = f"""
𝗕𝗜𝗡 ⇾ {cc[:6]}
𝗔𝗺𝗼𝘂𝗻𝘁 ⇾ {amount}

{astro}

𝗜𝗻𝗳𝗼: {bin_info}
"""

    await loading_message.delete()
    await message.reply(mess, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)

@app.on_message(filters.command("gen", prefixes="."))
async def generate_cc_command(client, message):
    await generate_cc(client, message)
    
