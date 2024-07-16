from pyrogram import Client, filters, enums
import psutil
from EQUROBOT import app

def get_sys_stats():
    uptime = psutil.boot_time()
    uptime_readable = datetime.datetime.fromtimestamp(uptime).strftime("%Hh:%Mm:%Ss")
    ram_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=1)
    disk_usage = psutil.disk_usage('/').percent
    pyrogram_calls = app.storage.stats['pyrogram']['global']
    return uptime_readable, ram_usage, cpu_usage, disk_usage, pyrogram_calls

@app.on_message(filters.command(["alive", "ping"], prefixes="."))
async def statuschk(client, message):
    uptime, ram_usage, cpu_usage, disk_usage, pyrogram_calls = get_sys_stats()

    await message.reply_text(f'''
**🏓 ᴩᴏɴɢ : {pyrogram_calls}ᴍs..**

➻ sʏsᴛᴇᴍ sᴛᴀᴛs :

↬ ᴜᴩᴛɪᴍᴇ : {uptime}
↬ ʀᴀᴍ : {ram_usage}%
↬ ᴄᴩᴜ : {cpu_usage}%
↬ ᴅɪsᴋ : {disk_usage}%
↬ ᴩʏ-ᴛɢᴄᴀʟʟs : {pyrogram_calls}ᴍs

🥀ʙʏ » <a href="https://t.me/YourExDestiny">ɪᴀᴍ_ᴅᴀxx ♡︎</a>
    ''', parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
