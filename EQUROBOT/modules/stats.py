import platform
import psutil
import time
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
    tmp = (((str(weeks) + "w:") if weeks else "") +
           ((str(days) + "d:") if days else "") +
           ((str(hours) + "h:") if hours else "") +
           ((str(minutes) + "m:") if minutes else "") +
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

@app.on_message(filters.command("stats"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    storage = psutil.disk_usage('/')
    platform_info = platform.platform()
    python_version = platform.python_version()
    py_tgcalls_version = "0.9.0"  # replace with actual version if known

    TEXT = (
        "┏━━━━━━━⍟\n"
        "┃**#BOTSTATS** ✅\n"
        "┗━━━━━━━━━━━⊛\n"
        f"⊙ **UPTIME** ➠ {uptime}\n"
        f"⊙ **CPU** ➠ {cpu}%\n"
        f"⊙ **RAM** ➠ {size_formatter(ram.total)}\n"
        f"⊙ **PHYSICAL CORES** ➠ {psutil.cpu_count(logical=False)}\n"
        f"⊙ **TOTAL CORES** ➠ {psutil.cpu_count(logical=True)}\n"
        f"⊙ **CPU FREQUENCY** ➠ {psutil.cpu_freq().current / 1000:.2f} GHz\n"
        f"⊙ **STORAGE AVAILABLE** ➠ {size_formatter(storage.total)}\n"
        f"⊙ **STORAGE USED** ➠ {size_formatter(storage.used)}\n"
        f"⊙ **STORAGE LEFT** ➠ {size_formatter(storage.free)}\n"
        f"⊙ **PYTHON VERSION** ➠ {python_version}\n"
        f"⊙ **PYROGRAM VERSION** ➠ {pyrogram_version}\n"
        f"⊙ **PLATFORM** ➠ {platform_info}\n"
    )

    await message.reply_video(
        video=PING_MP4,
        caption=TEXT,
    )
    
