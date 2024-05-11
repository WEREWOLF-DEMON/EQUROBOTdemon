import requests
import datetime
import telebot
import time
import mysql.connector
import json
from pyrogram import filters
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
from mysql.connector import Error
from EQUROBOT import app
from base64 import b64decode
from inspect import getfullargspec
from io import BytesIO
from aiohttp import ClientSession
from pyrogram.types import *

def find_captcha(response_text):
    if 'recaptcha' in response_text.lower():
        return ' Using Google reCAPTCHA ✅'
    elif 'hcaptcha' in response_text.lower():
        return 'Using hCaptcha ✅'
    else:
        return 'Not using Any Captcha🚫'

def detect_cloudflare(response):
    cloudfare_elements = ["cloudfare.com", "__cfduid"]
    for element in cloudfare_elements:
        if element in response.text.lower():
            return True
    cloudfare_headers = ["cf-ray", "cf-cache-status", "server"]
    for header in cloudfare_headers:
        if header in response.headers:
            return True
    return False

def find_payment_gateways(response_text):
    # Your implementation remains the same

def find_stripe_version(response_text):
    # Your implementation remains the same

def find_payment_gateway(url):
    # Your implementation remains the same

@app.on_message(filters.command("ck"))
async def check_payment_gateways(_, message):
    try:
        result_message = ""
        website_urls = [message.text[len('/ck'):].strip()]
        full = message.text.split(None, 2)[2].lower().strip() in [
            "yes",
            "y",
            "1",
            "true",
        ]
        if not website_urls[0].startswith(("http://", "https://")):
            website_urls[0] = "http://" + website_urls[0]  # Add http:// if not provided

        for website_url in website_urls:
            response = requests.get(website_url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            photo = await take_screenshot(website_url, full)
            if not photo:
                await message.reply("**ғᴀɪʟᴇᴅ ᴛᴏ ᴛᴀᴋᴇ sᴄʀᴇᴇɴsʜᴏᴛ.**")
                continue
            await message.reply_photo(photo, reply_markup=button)

            detected_gateways = find_payment_gateways(response.text)
            detected_captcha = find_captcha(response.text)
            is_cloudflare_protected = detect_cloudflare(response)

            result_message = f"----------------------------\n"
            result_message += f"|𝙍𝙚𝙨𝙪𝙡𝙩𝙨 𝙛𝙤𝙧 {website_url}:\n"
            result_message += f"|𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗚𝗮𝘁𝗲𝘄𝗮𝘆𝘀: {', '.join(detected_gateways)}\n"
            result_message += f"|𝗖𝗮𝗽𝘁𝗰𝗵𝗮: {detected_captcha}\n"
            result_message += f"|𝘾𝙡𝙤𝙪𝙙𝙛𝙡𝙖𝙧𝙚 𝙋𝙧𝙤𝙩𝙚𝙘𝙩𝙞𝙤𝙣: {'✅' if is_cloudflare_protected else '🚫'}\n"
            result_message += f"----------------------------\n"
        result_message += f"𝐁𝐨𝐭 𝐛𝐲 - @iam_daxx 👑\n"
        result_message += f"---------------------------\n"
        result_message += f"𝗖𝗛𝗘𝗖𝗞𝗘𝗗 𝗕𝗬 𝗧𝗘𝗔𝗠 @GITWIZARD\n"
        result_message += f"--------------------------------------------------------------\n"

        await message.reply(result_message)

    except requests.exceptions.RequestException as e:
        await message.reply("𝐄𝐫𝐫𝐨𝐫: 𝐈𝐧 𝐅𝐞𝐭𝐜𝐡𝐢𝐧𝐠 𝐃𝐞𝐭𝐚𝐢𝐥𝐬. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐡𝐞𝐜𝐤 𝐋𝐢𝐧𝐤 𝐢𝐟 𝐭𝐡𝐞 𝐥𝐢𝐧𝐤 𝐢𝐬 𝐫𝐞𝐚𝐜𝐡𝐚𝐛𝐥𝐞 𝐨𝐫 𝐧𝐨𝐭 ")


button = InlineKeyboardMarkup([[
            InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="close_data")
                              ]])

aiohttpsession = ClientSession()

async def post(url: str, *args, **kwargs):
    async with aiohttpsession.post(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data

async def take_screenshot(url: str, full: bool = False):
    url = "https://" + url if not url.startswith("http") else url
    payload = {
        "url": url,
        "width": 1100,
        "height": 1900,
        "scale": 1,
        "format": "jpeg",
    }
    if full:
        payload["full"] = True
    data = await post(
        "https://webscreenshot.vercel.app/api",
        data=payload,
    )
    if "image" not in data:
        return None
    b = data["image"].replace("data:image/jpeg;base64,", "")
    file = BytesIO(b64decode(b))
    file.name = "webss.jpg"
    return file
