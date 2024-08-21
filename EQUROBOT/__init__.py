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
    string_session="1BVtsOG4Bu6c2pWFuQHupAA0OhUOrkcs-GvI7D9G2qfqgb3DBLEuSwzrKh3bVQxVbJxiLWvT_qne4WJkreSSyjoevtxnLnYIFsMGoYOePhn3Ga7pJizhyPft-BJRkno9uyMzt8NGTqu1D_RtgAaKSzfUUSznoF2L3OMgKxwT1VMEpPFItgt6Mr4mfuhZuNh-9BuFuX0CxB7ENGnCy4G7Pw-eiq1nvjSiskuCe6YcQxvRaXdYQEq9HR14lD5Hc4NbV18xlo2s2xD77jkRO1coiQX0MkT1w5MEt2UAC7Xl7u0Cy8ZavQHrlIQJXZpUJZ-jMmlftQsb01HWPGK3ldJ0neb8_qS_KVfc="
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
