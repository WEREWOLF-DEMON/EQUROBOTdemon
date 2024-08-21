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
    BQCMuJEABV4RZTXJXdfRbxq8Buim4L4nAmhv7TW_hbFwLfKbFH0w5Crzq1AS19VGgM_IGV-1QdLnHrT128Z4HwQZyOgApDPQXjS6JDixAkjvL-8ECKJpCwi3HHfTKvcwp0nZT5BJFFhnlCYKJxREX1tYVOfFOQhbvC27TEa5zwu_4LRPeF7H0CGvrKw522UPuEoloRuoKgJ2VA-AVGt0pYjbxYZMQ801aPtDR3h6hHPL62g8eJQkLaPkSQN-i85hW3485Qf5OB-2MVETTNsv3Jix65ILH0aRShPxgdHKfBx3FmkPR_otR5v4QhwpJClDWtt8gqEERPvBeYlTYNu3jkWoMfy6-gAAAAFeTedSAA"
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
