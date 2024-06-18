from pyrogram import Client, filters, enums
import psutil
from EQUROBOT import app

def get_ram_usage():
    ram = psutil.virtual_memory()
    return ram.percent

def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

@app.on_message(filters.command("alive", prefixes="."))
async def statuschk(client, message):
    ram_usage = get_ram_usage()
    cpu_usage = get_cpu_usage()

    await message.reply_text(f'''
**🥀 I Aᴍ Aʟɪᴠᴇ Mʏ Dᴇᴀʀ Gᴇɴɪᴜs Mᴀsᴛᴇʀ ✨ ...**

[ϟ] 𝗝𝗘𝗧𝗧𝗜𝗫 𝗕𝗢𝗧 👑
[ϟ] 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦 : 𝗢𝗡 ✅
[ϟ] 𝗥𝗔𝗠 𝗨𝗦𝗔𝗚𝗘: <code>{ram_usage}%</code>
[ϟ] 𝗖𝗣𝗨 𝗨𝗦𝗔𝗚𝗘: <code>{cpu_usage}%</code>
[ϟ] 𝗕𝗢𝗧 𝗠𝗔𝗗𝗘 𝗕𝗬 : <a href="https://t.me/stripe_op">𝙋𝙞𝙖𝙨𝙝</a>
    ''', parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
