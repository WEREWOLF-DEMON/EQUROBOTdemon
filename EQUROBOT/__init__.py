import asyncio
import logging
import time
from importlib import import_module
from os import listdir, path
from dotenv import load_dotenv
from pyrogram import Client
from pyromod import listen
from config import API_ID, API_HASH, BOT_TOKEN, BOT_USERNAME, OWNER_ID, GPT_API, LOGGER_ID, DEEP_API

from SafoneAPI import SafoneAPI

safone = SafoneAPI()


loop = asyncio.get_event_loop()

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)



app = Client(
    ":EQUROBOT:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

scr = Client(
    "scr",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string="BAHEC1EAit9W6g0MF0_qDPBVEVGnfQ7rkyN18oW-I3rlaK1Y80AlfVQqjJtoJKUMxW6GuRtE2ZSeV7qUy10C6AhmScogRkzZZUqEJmGKdqObMKCTL7Md4ZEBbPkI_qNhBv1_auX1ISQbbtti1jcQ1VMJrhnnHwjEG_Okv6UrO8bk6hteHQ-uyNkVZGSdzWbExyaEXm3HarE_zCECLs7Lezix-O0LDQO5bcAR829OfygjXBDVwdnKjxwKO5-FztEG5kbcFWWN4z9VHFUA8B71XPMjNymthP7C6C25XMW3isu3lKptcTIqb5WgMeToRlDt8uuSdt03u_LblinxnDQiCZlo2g8YTQAAAAF7pDhJAA"
)



async def info_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    await scr.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(info_bot())
