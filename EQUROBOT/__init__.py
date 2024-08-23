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
    session_string="BQF1_JUAfDIQopgOc0Oan79zOi2QGpJOw0XqCmDMTscNKDlryBZcHw9X1NGBqJvDsaWbSYqaFVnQDwF_HcMK4haNSrIfn2YXM64ZC5Jd5KtiktXX-tSNTk0b4y4t8wBMCWNzw-YZcBJ2BbwPe5YotHH4sAN4S2-3c2bguWoo3pMyHE6RdlJSJ7B6nEHpgrnaVY12wIpnHHdW7_2bXQohHTub_Kr-X_mry1EX3N4QqTVo9Yne-QvhrVuK_R9skv4iPpNV3qv0wpeXXZs6W2iz3azuS9Tltkde0L9MLSq8DwPbP0g_0IjPEZUIZeQEJ2fYbdZxqHehYRfx99tBv-BUTIv_tuTjogAAAABpRCaiAA"
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
