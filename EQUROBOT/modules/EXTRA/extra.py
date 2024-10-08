from EQUROBOT import app
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import asyncio, os, time, aiohttp, random, requests
from requests.adapters import HTTPAdapter, Retry
from EQUROBOT.core.mongo import *
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import OWNER_ID, BOT_USERNAME
import pytz
import time
from datetime import datetime, timedelta
import config
import httpx
from pymongo import MongoClient
import re
from datetime import datetime
from gpytranslate import Translator

#-----------
@app.on_message(filters.command("table"))
def multiplication_table(_, message: Message):
    try:
        
        number = int(message.text.split()[1])

        table = "\n".join([f"{number} x {i} = {number * i}" for i in range(1, 11)])

        
        message.reply_text(f"Multiplication table of {number}:\n\n{table}")
    except IndexError:
        message.reply_text("Please enter a valid number after the command /table.")
    except ValueError:
        message.reply_text("Invalid input. Please enter a valid number.")



#-----------



@app.on_message(filters.video_chat_started)
async def brah(_, msg):
       await msg.reply("**🎙️ 𝖵𝗈𝗂𝖼𝖾 𝖼𝗁𝖺𝗍 𝗌𝗍𝖺𝗋𝗍𝖾𝖽!**")

# ----------------------------------------------------------------------------------
# --------------------------------------------------------------------------------- #
@app.on_message(filters.video_chat_ended)
async def brah2(_, msg):
       await msg.reply("**🔇 𝖵𝗈𝗂𝖼𝖾 𝖼𝗁𝖺𝗍 𝖾𝗇𝖽𝖾𝖽. 𝖳𝗁𝖺𝗇𝗄𝗌 𝖿𝗈𝗋 𝗃𝗈𝗂𝗇𝗂𝗇𝗀**")

# ----------------------------------------------------------------------------------
# --------------------------------------------------------------------------------- #
@app.on_message(filters.video_chat_members_invited)
async def brah3(app :app, message:Message):
           text = f"{message.from_user.mention} ɪɴᴠɪᴛᴇᴅ "
           x = 0
           for user in message.video_chat_members_invited.users:
             try:
               text += f"[{user.first_name}](tg://user?id={user.id}) "
               x += 1
             except Exception:
               pass
           try:
             await message.reply(f"{text} ☄️")
           except:
             pass


#-----------------

@app.on_message(filters.command('id'))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )


#--------------------------------------------------------------------------------------
mongo_url_pattern = re.compile(r'mongodb(?:\+srv)?:\/\/[^\s]+')


@app.on_message(filters.command("mongochk"))
async def mongo_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please enter your MongoDB URL after the command. Example: /mongochk YOUR_MONGO_URL")
        return

    mongo_url = message.command[1]
    if re.match(mongo_url_pattern, mongo_url):
        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            client.server_info()
            await message.reply("MongoDB URL is valid and connection successful ✅")
        except Exception as e:
            await message.reply(f"Failed to connect to MongoDB: {e}")
    else:
        await message.reply("Invalid MongoDB URL format. Please enter a valid MongoDB URL💔")


# ---------------------------------------------------------------------

@app.on_message(filters.command('info'))
async def myinfo_command(client, message):
    user = message.from_user

    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            user = await app.get_users(user_id)
        except ValueError:
            await app.send_message(chat_id=message.chat.id, text="Invalid user ID.")
            return
    premium = "OWNER" if user.id == OWNER_ID else ("PREMIUM" if await has_premium_access(user.id) else "FREE")
    use = await check_remaining_uasge(user.id)
    expiry_ist = (datetime.now() + use).astimezone(pytz.timezone("Asia/Kolkata"))
    expire = expiry_ist.strftime("%d-%m-%Y\n✦ **EXPIRY TIME:** %I:%M:%S %p")
    user_info = (
        f"┏━━━━━━━⍟━━━━━━━━━━━┓\n"
        f"┃ 🌟 **𝖸𝗈𝗎𝗋 𝖨𝗇𝖿𝗈 𝗈n EQUROBOT** 🌟  \n"
        f"┗━━━━━━━━━⊛━━━━━━━━━┛\n"
        f"\n"
        f"**🧑 User Info**\n"
        f"✦ **ID:** `{user.id}`\n"
        f"✦ **Username:** @{user.username}\n"
        f"✦ **First Name:** {user.first_name}\n"
        f"✦ **Last Name:** {user.last_name}\n"
        f"✦ **Mention:** {user.mention}\n"
        f"✦ **𝖳𝖦 𝖲𝖼𝖺𝗆𝗍𝖺𝗀:** {'✅' if user.is_scam else '❌'}\n"
        f"✦ **𝖳𝖦 𝖯𝗋𝖾𝗆𝗂𝗎𝗆:** {'✅' if user.is_premium else '❌'}\n"
        f"✦ **Plan Status:** {premium}\n"
        f"✦ **PLAN EXPIRY:** {expire}\n"
    )
    await message.reply_text(text=user_info)


# ---------------------------------------------------------------------

@app.on_message(filters.command("lg") & filters.user(config.OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    await message.reply_text("Your bot has successfully left the chat 🙋‍♂️")
    await app.leave_chat(chat_id=chat_id, delete=True)



# ------------

#.......

trans = Translator()

#......

@app.on_message(filters.command("tr"))
async def translate(_, message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ɪᴛ !")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"ᴛʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {source} to {dest}:\n"
        f"{translation.text}"
    )
    await message.reply_text(reply)
