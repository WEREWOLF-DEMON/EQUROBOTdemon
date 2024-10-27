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
    session_string="BQF1_JUAYLIGOFGN7Mu20yZKBZZ0NCPNcbRnFUxt7YJFPlKbARbBUZ_b96zIGxKqgLolOl6zRZnYiMFUyLaU2oXnN10midGc782O2HOIIt6GxJbKurnpF5IiZPQ9DEmBDihyTz7lLAMZba0xd9O95krKzJ52it9-_ZtGgdIsK9PKy6izB2J07sNDxVvsk2uPo5PFpyw4rt63nW3fYGh2Bu5LoxBBY-6KGJmQJTdhwvaPE3IHbl1BGLh0OUj816wPr3MFh_2vTu3tO7nps_rYzRZsytumTGr16AuB3Uv5VWE274kOAmYhnBayPxrufGR3-pptI2mvKNuA-dY2uA8C-ne2zhXq0AAAAAHNyayXAA"
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
