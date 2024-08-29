import time
from urllib.parse import urlparse
import os
import asyncio
import requests
import wget
from youtubesearchpython import SearchVideos
from youtube_search import YoutubeSearch
from pytube import YouTube
from pyrogram import filters
from pyrogram.types import *
from EQUROBOT import app

def download_video(url):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        output_file = video_stream.download(filename=f"{yt.video_id}.mp4")
        return yt
    except Exception as e:
        raise e

@app.on_message(filters.command("song"))
async def download_song(_, message):
    query = " ".join(message.command[1:])
    m = await message.reply("**🔄 sᴇᴀʀᴄʜɪɴɢ... **")
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
        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        audio_file = audio_stream.download(filename=f"{yt.video_id}.m4a")

        duration_sec = yt.length

        await m.edit("**📤 ᴜᴘʟᴏᴀᴅɪɴɢ...**")
        await message.reply_audio(
            audio_file,
            thumb=thumb_name,
            title=title,
            caption=f"{title}\nRᴇǫᴜᴇsᴛᴇᴅ ʙʏ ➪{message.from_user.mention}\nVɪᴇᴡs➪ {views}\nCʜᴀɴɴᴇʟ➪ {channel_name}",
            duration=duration_sec
        )
        await m.delete()
    except Exception as e:
        await m.edit(" - An error occurred!!")
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
    """Extract Text From Commands"""
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

        yt = download_video(url)
        
        c_time = time.time()
        file_stark = f"{yt.video_id}.mp4"
        capy = f"❄ **ᴛɪᴛʟᴇ :** [{thum}]({mo})\n💫 **ᴄʜᴀɴɴᴇʟ :** {thums}\n✨ **sᴇᴀʀᴄʜᴇᴅ :** {urlissed}\n🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {chutiya}"
        await client.send_video(
            message.chat.id,
            video=open(file_stark, "rb"),
            duration=int(yt.length),
            file_name=str(yt.title),
            thumb=sedlyf,
            caption=capy,
            supports_streaming=True,
        )
        await pablo.delete()
        for files in (sedlyf, file_stark):
            if files and os.path.exists(files):
                os.remove(files)
    except Exception as e:
        await pablo.edit(f"**ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.** \n**ᴇʀʀᴏʀ :** `{str(e)}`")

__mod_name__ = "Vɪᴅᴇᴏ"
__help__ = """ 
/video to download video song
/yt to download video song """
