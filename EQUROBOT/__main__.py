import asyncio
import importlib
from pyrogram import idle
from EQUROBOT import app
from EQUROBOT.modules import ALL_MODULES
import config
from config import LOGGER_ID

loop = asyncio.get_event_loop()

async def daxxpapa_boot():
    for all_module in ALL_MODULES:
        # Extract only the module name (first element of the tuple)
        module_name = all_module[0]  # all_module is a tuple, we need the module name
        importlib.import_module("EQUROBOT.modules." + module_name)
    print("𝖻𝗈𝗍 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅 𝗌𝗍𝖺𝗋𝗍")
    
    # Send message when the bot starts
    await app.send_message(LOGGER_ID, "**𝖨 𝖺𝗆 𝖺𝗅𝗂𝗏𝖾 𝖡𝖺𝖻𝗒 𝖸𝗈𝗎𝗋 𝖡𝗈𝗍 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅 𝖣𝖾𝗉𝗅𝗈𝗒 \n Mʏ Dᴇᴠᴇʟᴏᴘᴇʀ  [𝐌𝚁°᭄𝐃𝙰𝚇𝚇 ࿐™ ](https://t.me/YourExDestiny)**")
    
    # Keep the bot running
    await idle()
    print("𝖻𝖺𝗁𝖺𝗇𝖼𝗁𝗈𝖽 𝖯𝗂𝗋𝗈 𝖢𝗈𝖽𝖾𝗋 𝗄𝗋𝗅𝗈 𝖾𝖽𝗂𝗍 𝖺𝖺 𝗀𝗒𝖺 𝗇 𝖾𝗋𝗋𝗈𝗋 𝖺𝖺𝖻 𝗃𝖺𝗄𝖾 𝗀𝗂𝗋𝗅𝗈 @YourExDestiny")

if __name__ == "__main__":
    # Properly call loop.run_until_complete with the function
    loop.run_until_complete(daxxpapa_boot())
    
