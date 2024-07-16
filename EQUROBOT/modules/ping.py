import platform
import config
import psutil
import time
from pyrogram.types import InputMediaVideo
import random
from EQUROBOT import app as daxxop
from pyrogram import Client, filters
from pyrogram.types import Message


start_time = time.time()

PING_MP4 = "https://telegra.ph/file/756b031774cb4382f181c.mp4"

def time_formatter(milliseconds):
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (((str(weeks) + "ᴡ:") if weeks else "") +
           ((str(days) + "ᴅ:") if days else "") +
           ((str(hours) + "ʜ:") if hours else "") +
           ((str(minutes) + "ᴍ:") if minutes else "") +
           ((str(seconds) + "s") if seconds else ""))
    if not tmp:
        return "0s"
    if tmp.endswith(":"):
        return tmp[:-1]
    return tmp

def size_formatter(bytes, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(bytes) < 1024.0:
            return "%3.1f %s%s" % (bytes, unit, suffix)
        bytes /= 1024.0
    return "%.1f %s%s" % (bytes, 'Y', suffix)

def get_db_stats():
    client = pymongo.MongoClient("mongodb+srv://tanujaXmusic:tanujaXmusic@tanujaXmusic.octnw1p.mongodb.net/")
    db = client.get_database()
    stats = db.command("dbstats")
    return stats

@app.on_message(filters.command("ping"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    storage = psutil.disk_usage('/')
    platform_info = platform.platform()
    python_version = platform.python_version()
    pyrogram_version = Client.__version__
    py_tgcalls_version = "0.9.0"  # replace with actual version if known
    db_stats = get_db_stats()

    TEXT = (
       "**๏─╼⃝𖠁๏𝖯𝖨𝖭𝖦🏓 𝖯𝖮𝖭𝖦๏𖠁⃝╾─๏**\n\n"
        f" ⦿ 𝖴𝖯𝖣𝖠𝖳𝖤 🔄 ➠ {uptime}\n"
        f" ⦿ 𝖢𝖯𝖴 ⚙️ ➠ {cpu}%\n"
        f" ⦿ 𝖱𝖠𝖬 💾 ➠ {size_formatter(ram.total)}\n"
        f" ⦿ 𝖯𝖧𝖸𝖲𝖨𝖢𝖠𝖫 𝖢𝖮𝖱𝖤𝖲 🖥️ ➠ {psutil.cpu_count(logical=False)}\n"
        f" ⦿ 𝖳𝖮𝖳𝖠𝖫 𝖢𝖮𝖱𝖤𝖲 🖥️ ➠ {psutil.cpu_count(logical=True)}\n"
        f" ⦿ 𝖢𝖯𝖴 𝖥𝖱𝖤𝖰 🖥️ ➠ {psutil.cpu_freq().current / 1000:.2f} GHz\n"
        f" ⦿ 𝖲𝖳𝖮𝖱𝖠𝖦𝖤 𝖠𝖵𝖠𝖨𝖫𝖠𝖡𝖫𝖤 🗃️ ➠ {size_formatter(storage.total)}\n"
        f" ⦿ 𝖲𝖳𝖮𝖱𝖠𝖦𝖤 𝖴𝖲𝖤𝖣 📊 ➠ {size_formatter(storage.used)}\n"
        f" ⦿ 𝖲𝖳𝖮𝖱𝖠𝖦𝖤 𝖫𝖤𝖥𝖳 🗃️ ➠ {size_formatter(storage.free)}\n"
        f" ⦿ 𝖯𝖸𝖳𝖧𝖮𝖭 𝖵𝖤𝖱𝖲𝖨𝖮𝖭 🐍 ➠ {python_version}\n"
        f" ⦿ 𝖯𝖸𝖱𝖮𝖦𝖱𝖠𝖬 ➠ {pyrogram_version}\n"
        f" ⦿ 𝖯𝖸-𝖳𝖦𝖢𝖠𝖫𝖫𝖲 ➠ {py_tgcalls_version}\n"
        f" ⦿ 𝖯𝖫𝖠𝖳𝖥𝖮𝖱𝖬 🖥️ ➠ {platform_info}\n\n"
        f" ⦿ 𝖳𝖮𝖳𝖠𝖫 𝖣𝖡 𝖲𝖨𝖹𝖤 🗃️ ➠ {db_stats['storageSize'] / (1024*1024):.2f} MB\n"
        f" ⦿ 𝖳𝖮𝖳𝖠𝖫 𝖣𝖡 𝖲𝖳𝖮𝖱𝖠𝖦𝖤 🗃️ ➠ {db_stats['dataSize'] / (1024*1024):.2f} MB\n"
        f" ⦿ 𝖳𝖮𝖳𝖠𝖫 𝖣𝖡 𝖢𝖮𝖫𝖫𝖤𝖢𝖳𝖨𝖮𝖭𝖲 📚 ➠ {db_stats['collections']}\n"
        f" ⦿ 𝖳𝖮𝖳𝖠𝖫 𝖣𝖡 𝖪𝖤𝖸𝖲 🗝️ ➠ {db_stats['objects']}\n"
    )

    await message.reply_video(
        video=PING_MP4,
        caption=TEXT,
    )
    
