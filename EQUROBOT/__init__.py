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
"""
scr = Client(
    "scr",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string="BQGoLIMAOKXVTjaGOZN_8kShQdKccRd7HA-44GV5eLHHMW-x5wkMEWQHeNeymWRAp-Zml2tZZ8OjP8s-1_eLLKZiJTud9Nm8KO6iBNw_n91qB0tob5XfHcP9VRl1Yd97cCXOMv-wiQNNEN_APBKTGTrSdoEJxyv7RymmlhBSvmxmnIaewzSNR9rUE7SCojVWYskW01O7ootmaa41nPSJgFjfAn0bUGRI838LlbkDpxVuBqb83BTTunwBNlddBXmm10dm2aw7CaVf9JrCyn_X9dhB0YGoanFGqXFYGKpj7nshJ4djVN8MHtLRB3oKWQ7jQUKE4L6S8WVkyic0_5KqBj7tc_4gxQAAAAGw_lmDAA"
)
"""


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
