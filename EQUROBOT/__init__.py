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
    session_string="BQGNW3cAO3MR4N-Jb1tjbuxxpqe1IrDIMZ913ow4ZrZKgz5yiyKGtGQixSCPMgVGl2_nmEzD14jQCE1iegtopV82nTCPwDwOQQap8JVufOwJjhmg7gMGJm-PZSnALQHd3UHAmae9dzYDQasFvNb6SrFmCC_OhkwASmkZRHcD9a4TsmviDRQJfVZ8EhPGXmNpRMX8DUeZofqozDp1CI7b37GoL0lAc0aQgmhKEPpbTnJuchnv1L_OKezPQBdar6fBuJeKY8j3HDFQtplc_Dri0WD-fOKJwabkfODarCqffpqMlpu3usk9o1jT63PaGbSa2JxhRcTQEW9OmzpZV3i_DBkv1OZYawAAAAGsWT5mAA"
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
