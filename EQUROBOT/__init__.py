import asyncio
import logging
import time
from importlib import import_module
from os import listdir, path
from dotenv import load_dotenv
from pyrogram import Client
from pyromod import listen
#from EQUROBOT import app
from config import API_ID, API_HASH, BOT_TOKEN, BOT_USERNAME, OWNER_ID, GPT_API, LOGGER_ID, DEEP_API
from EQUROBOT.modules.clonedb import restart_bots
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
    session_string="BQF1_JUArYrW6_aliyL4s03B9foEOvE5iOB1WpvGlI5YcEEqhx8mzZGrQkjHGGHymLp3sPCS03DCLDDFN_PbMavY_DY9CmTyko1W_K6X2FSIf54J2wESvZFrJ7xV89EVdZCmYqGWVccIXhmABUjEP8AYRgbDOpvbdbkA1s0BObRj_i2_TUZjxlm3RHKqUoZ5kvnd4tWk8kb-BFp3qQTW32eFgl6vBJXcsQ3o50l1C_CyUm7PdGP3iBdk96wBCQ3YU4ZsgniJXJ6_Pm4dAjSenkgAqRmeAUNdjlMCMfipg4Vv0ElaQzqLfrH6hcOukxvZvZIPlADpQ69yShAWQQGLHGih0sdl-wAAAAGlC9VZAA"
)



async def info_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    await scr.start()
    await restart_bots()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(info_bot())
