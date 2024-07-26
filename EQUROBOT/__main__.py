import asyncio
import importlib
from pyrogram import Client, idle
import config
from config import LOGGER_ID
from EQUROBOT.modules import ALL_MODULES
from EQUROBOT.modules.clonedb import restart_bots

loop = asyncio.get_event_loop()

# Initialize the app here to avoid circular import issues
app = Client(
    ":EQUROBOT:",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)

async def daxxpapa_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("EQUROBOT.modules." + all_module)
    print("Bot successfully started")
    await app.start()
    await restart_bots()
    await app.send_message(LOGGER_ID, "**I am alive! Your bot has been successfully deployed.\nMy Developer: [𝐌𝚁°᭄𝐃𝙰𝚇𝚇 ࿐™](https://t.me/YourExDestiny)**")
    await idle()
    await app.stop()
    print("Shutting down...")

if __name__ == "__main__":
    loop.run_until_complete(daxxpapa_boot())
