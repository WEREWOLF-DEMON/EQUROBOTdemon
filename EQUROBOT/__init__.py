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
    session_string="BQF1_JUAp09Ps9lIrFa7UdaarrFSKyLh49SZkFpDF141OKKqm6YGoRqfqKNwn11hQUSHb1DEJWIejjIgerX29G18VYPuFwUZU1aZlj06dbhwV8H2MbX7faLr_U_fF9VvvkH80HNrNaT33kRsewhedxBgRwMtn8Eg6TegrZbWYZIh8nF3H1jBw7h1pJOey8IeD3gSteFIt1onh2A6oRIGo2jzlsVJ5E6wOQ3tW73wgyYQQbczc4GkVnMOc7diKIphfHAueyFmB3czLPWc8SXc1mzGJo1R4R62z74bw9tQa7Q0woOtatCwD5Zux1XNCAFKSQMqXUUEqwNKDBYcE8fLkG4JdCkYwQAAAABpRCaiAA"
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
