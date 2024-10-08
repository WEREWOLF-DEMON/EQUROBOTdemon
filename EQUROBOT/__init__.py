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
    session_string="BAEBfSYAbKz5o1nh4FyxCjGs8AKMKIMTM_451xF6NcMYR-W40XinOifGNsLPOhbFbUnF1Di89Lf4Y8ha2vmotzcp2Au7meuoMH12Egr8PhRgPusrnAS61bB6Pw_FPeYdcmvm-GvH71JUHl-SqofmJcKKxCfw3mx15fjOsOXmuP2zaAjoajjk5XKMhLAA62rfohlyc6TTEVp4H5qUvSLYlBITUAKvErN8ep1XH3bp8tKoIssdWqEvWWBSXXQMGhz63wF5A4_aFw_L_eZkPKvHCVcY3zGO0lpT2qoHQCfSicI9Im6aN6RenoSdllVtdxkiFB9YiBsOUoEhC1KJ77TTIhLpBtde8AAAAAF7pDhJAA"
)



async def info_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    #await scr.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(info_bot())
