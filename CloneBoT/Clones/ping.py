from pyrogram import Client, filters, enums
import psutil
from EQUROBOT import app

def get_ram_usage():
    ram = psutil.virtual_memory()
    return ram.percent

def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

@app.on_message(filters.command("ping", prefixes="."))
async def statuschk(client, message):
    ram_usage = get_ram_usage()
    cpu_usage = get_cpu_usage()

    await message.reply_text(f'''
I ᴀᴍ ᴀʟɪᴠᴇ, ᴍʏ ᴅᴇᴀʀ ɢᴇɴɪᴜs ᴍᴀsᴛᴇʀ.

ᴇǫᴜʀᴏʙᴏᴛ
ʙᴏᴛ sᴛᴀᴛᴜs: ᴏɴ ✅
ʀᴀᴍ ᴜsᴀɢᴇ: {ram_usage}%
ᴄᴘᴜ ᴜsᴀɢᴇ: {cpu_usage}%
ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ: [ᴍʀ°᭄ᴅᴀxx ࿐](https://t.me/YourExDestiny)
    ''', parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
