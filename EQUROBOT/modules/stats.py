import platform
import psutil
import time
import pymongo
from pyrogram.types import InputMediaVideo
from EQUROBOT import app
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import __version__ as pyrogram_version  # Import pyrogram version

start_time = time.time()

PING_MP4 = "https://graph.org/file/e67795f5e68ed4b93ffea.mp4"

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
    client = pymongo.MongoClient("mongodb+srv://MRDAXX:MRDAXX@mrdaxx.prky3aj.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database('your_database_name')  # Specify your database name
    stats = db.command("dbstats")
    return stats

@Client.on_message(filters.command("stats"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    storage = psutil.disk_usage('/')
    platform_info = platform.platform()
    python_version = platform.python_version()
    py_tgcalls_version = "0.9.0"  # replace with actual version if known
    db_stats = get_db_stats()

    TEXT = (
       "**๏sᴛᴀᴛs ᴀɴᴅ ɪɴғᴏʀᴍᴀᴛɪᴏɴ๏**\n\n"
        f" ⦿ ᴜᴘᴅᴀᴛᴇ 🔄 ➠ {uptime}\n"
        f" ⦿ ᴄᴘᴜ ⚙️ ➠ {cpu}%\n"
        f" ⦿ ʀᴀᴍ 💾 ➠ {size_formatter(ram.total)}\n"
        f" ⦿ ᴘʜʏsɪᴄᴀʟ ᴄᴏʀᴇs 🖥️ ➠ {psutil.cpu_count(logical=False)}\n"
        f" ⦿ ᴛᴏᴛᴀʟ ᴄᴏʀᴇs 🖥️ ➠ {psutil.cpu_count(logical=True)}\n"
        f" ⦿ ᴄᴘᴜ ғʀᴇǫ 🖥️ ➠ {psutil.cpu_freq().current / 1000:.2f} GHz\n"
        f" ⦿ sᴛᴏʀᴀɢᴇ ᴀᴠᴀɪʟᴀʙʟᴇ 🗃️ ➠ {size_formatter(storage.total)}\n"
        f" ⦿ sᴛᴏʀᴀɢᴇ ᴜsᴇᴅ 📊 ➠ {size_formatter(storage.used)}\n"
        f" ⦿ sᴛᴏʀᴀɢᴇ ʟᴇғᴛ 🗃️ ➠ {size_formatter(storage.free)}\n"
        f" ⦿ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ 🐍 ➠ {python_version}\n"
        f" ⦿ ᴘʏʀᴏɢʀᴀᴍ ➠ {pyrogram_version}\n"
        f" ⦿ ᴘʏ-ᴛɢᴄᴀʟʟs ➠ {py_tgcalls_version}\n"
        f" ⦿ ᴘʟᴀᴛғᴏʀᴍ 🖥️ ➠ {platform_info}\n\n"
        f" ⦿ ᴛᴏᴛᴀʟ ᴅʙ sɪᴢᴇ 🗃️ ➠ {db_stats['storageSize'] / (1024*1024):.2f} MB\n"
        f" ⦿ ᴛᴏᴛᴀʟ ᴅʙ sᴛᴏʀᴀɢᴇ 🗃️ ➠ {db_stats['dataSize'] / (1024*1024):.2f} MB\n"
        f" ⦿ ᴛᴏᴛᴀʟ ᴅʙ ᴄᴏʟʟᴇᴄᴛɪᴏɴs 📚 ➠ {db_stats['collections']}\n"
        f" ⦿ ᴛᴏᴛᴀʟ ᴅʙ ᴋᴇʏs 🗝️ ➠ {db_stats['objects']}\n"
    )

    await message.reply_video(
        video=PING_MP4,
        caption=TEXT,
    )
    
