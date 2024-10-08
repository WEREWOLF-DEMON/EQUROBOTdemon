import asyncio
import importlib
from pyrogram import idle
from EQUROBOT import app
from EQUROBOT.modules import ALL_MODULES
from config import LOGGER_ID

loop = asyncio.get_event_loop()

async def daxxpapa_boot():
    for all_module in ALL_MODULES:
        module_name = all_module[0]  # Extract module name from tuple
        try:
            importlib.import_module("EQUROBOT.modules." + module_name)
            print(f"Successfully imported: {module_name}")
        except Exception as e:
            print(f"Failed to import module {module_name}: {str(e)}")

    print("Bot successfully started")
    await app.send_message(
        LOGGER_ID,
        "**I am alive! Your bot has been successfully deployed. \n"
        "My Developer: [𝐌𝚁°᭄𝐃𝙰𝚇𝚇 ࿐™](https://t.me/YourExDestiny)**"
    )
    await idle()
    print("Bot stopped")

if __name__ == "__main__":
    loop.run_until_complete(daxxpapa_boot())
    
