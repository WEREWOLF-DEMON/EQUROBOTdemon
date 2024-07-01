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
    session_string="BQC6kfsAHYAX81Yg61rP01K9FPavjslDQ-5CLkaiEuqNXhRwS5BOJQFhrxeaZr0oZfI5FJBJKz2Mj8SNtmFe08nsUnJN8JrvoAlc5zxEhshWNJP5M4_7qjgVy8Q2Z12AA0od8iSAyDQkJZnNsCk73Mv53alNvPqeo8TIxC_v4SEMicpU8RUipxLKt57S_q15B2_amDN8cu2pXlf0Hhj770wwYV-JPLQ8eIpRsaJ_8NTBNfXkvlS_rdVKSboA99XnSkLo--25erheCBAGXf1wKtOWgXUjxE3HmJz8-Ppjo_mB459H9A215LOOEjyl7nLTaQGuBS6yxtpPCT-qKg_wDAQTnXnHrgAAAAGkC4T6AA"
)

scr2 = Client(
    "scr2",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string="AQAaqk4Afm17ws0m_fBUAsI2o5LKf1E0I2RZIDryt-ZnKMMw0Fz7d_GH3pK-cllAigJDnnhW8b66SxmCf2m4Gxl9QiuCkrX3dwEDAFwgUrU5fUPUzCf-rCYUdw4bRGrL8BNcEZn8ezHznlMDaylo6hP71De0d557tlPbIr7lQInPhqo7-r7I_s0JtMgaajXd4H9gz1xqX1dorXG8EY9qVIfCBz6SQjpfHxKVpcoA0Dh_ClHukGMySKMCQqPczVmz3TJnlCp25RNn5hwYGRFs3gGTsofYS7DpjmCEn06MsbmjXB4co3nJRzD35IBZ-7VChlzxjFQWEO0FLWX8-VAEHOJkRX4ArQAAAAGE_Y--AA"
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
