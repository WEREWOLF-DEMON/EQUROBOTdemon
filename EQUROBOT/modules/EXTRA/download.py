import os
import time
import asyncio
import requests
import wget
import yt_dlp
from youtubesearchpython import SearchVideos
from youtube_search import YoutubeSearch
from pyrogram import filters
from pyrogram.types import *
from EQUROBOT import app

# Function to download a video using cookies for authentication
def download_video(url):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",  # Updated to get the best quality available, including 4K
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
        "proxy": "http://purevpn0s13830845:6phsLWXBQEq4MR@prox-in.pointtoserver.com:10799"
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
            infoo = ytdl.extract_info(url, download=True)
            return infoo
    except Exception as e:
        raise e

@app.on_message(filters.command("song"))
async def download_song(_, message):
    query = " ".join(message.command[1:])
    m = await message.reply("**🔄 sᴇᴀʀᴄʜɪɴɢ... **")
    ydl_ops = {
        "format": "bestaudio[ext=m4a]",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "192",
        }]
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        views = results[0]["views"]
        channel_name = results[0]["channel"]
    except Exception as e:
        await m.edit("**⚠️ ɴᴏ ʀᴇsᴜʟᴛs ᴡᴇʀᴇ ғᴏᴜɴᴅ. ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ sᴏɴɢ ɴᴀᴍᴇ**")
        return
    await m.edit("**📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("**📤 ᴜᴘʟᴏᴀᴅɪɴɢ...**")
        await message.reply_audio(
            audio_file,
            thumb=thumb_name,
            title=title,
            caption=f"{title}\nRᴇǫᴜᴇsᴛᴇᴅ ʙʏ ➪{message.from_user.mention}\nVɪᴇᴡs➪ {views}\nCʜᴀɴɴᴇʟ➪ {channel_name}",
            duration=dur
        )
        await m.delete()
    except Exception as e:
        await m.edit(" - An error !!")
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        pass

def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]

def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

@app.on_message(filters.command(["yt", "video"]))
async def ytmusic(client, message: Message):
    try:
        urlissed = get_text(message)
        await message.delete()
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        chutiya = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        pablo = await client.send_message(message.chat.id, f"sᴇᴀʀᴄʜɪɴɢ, ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ...")
        if not urlissed:
            await pablo.edit(
                "😴 sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ ᴏɴ ʏᴏᴜᴛᴜʙᴇ.\n\n» ᴍᴀʏʙᴇ ᴛᴜɴᴇ ɢᴀʟᴛɪ ʟɪᴋʜᴀ ʜᴏ, ᴩᴀᴅʜᴀɪ - ʟɪᴋʜᴀɪ ᴛᴏʜ ᴋᴀʀᴛᴀ ɴᴀʜɪ ᴛᴜ !"
            )
            return
        search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
        mi = search.result()
        mio = mi["search_result"]
        mo = mio[0]["link"]
        thum = mio[0]["title"]
        fridayz = mio[0]["id"]
        thums = mio[0]["channel"]
        kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
        await asyncio.sleep(0.6)
        url = mo
        sedlyf = wget.download(kekme)
        infoo = download_video(url)
        ytdl_data = infoo

        c_time = time.time()
        file_stark = f"{ytdl_data['id']}.mp4"
        capy = f"❄ **ᴛɪᴛʟᴇ :** [{thum}]({mo})\n💫 **ᴄʜᴀɴɴᴇʟ :** `{thums}`\n🍁 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {chutiya}"
        await pablo.edit("🔎 Fᴏᴜɴᴅ Sᴏᴍᴇᴛʜɪɴɢ Wᴀɪᴛ...")
        await client.send_video(
            message.chat.id,
            video=file_stark,
            caption=capy,
            supports_streaming=True,
            height=720,
            width=1280,
            thumb=sedlyf,
            duration=int(ytdl_data["duration"]),
            progress_args=(pablo, c_time, f"Uploading {urlissed} By.."),
        )
        await pablo.delete()
        try:
            os.remove(file_stark)
            os.remove(sedlyf)
        except:
            pass
    except Exception as e:
        await message.reply(f"{e}")
