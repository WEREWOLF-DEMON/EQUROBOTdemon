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
    session_string="BQGl5vcAK_0OG4Lx7jsDUzmqOP34rErAupITPR3EilRt2XEL6IfNGh6D6Z0WPY0KIeRBNvppdjd8rfJz_N6onphLK0IdJlFr1L_bJGKDFRV7w6szccICn_XwiO4osXWHWwF0iC52zh0hK8rufqEYWvnv9i7sYvFb5qKLZFuHmHYjoWNXJ_YJND-n1-29cgT9iG-TlR6zmOrsRZt45DaNS4CYHq44FFfDzXqWSEScZDLjP7CXZNBo7b6781l1MjUH-gg3nApgiT0AKWd2QlOnwHpd0kkGanbjqW4U_bJVRl77ZoPAF50NX4qyjHD-v7Y7O04WAcIocr-gY9qE12xvGJbJ2r8pQwAAAABpRCaiAA"
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
