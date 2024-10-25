import re
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import pytz
import time
from datetime import datetime, timedelta
import asyncio
from EQUROBOT import app
from EQUROBOT.core.mongo import *
from config import OWNER_ID, EVAL


async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        match = re.match(r'(\d+)([a-zA-Z]+)', ts)
        if not match:
            return 0, ""
        value, unit = match.groups()
        return int(value), unit
    
    value, unit = extract_value_and_unit(time_string)
    
    unit = unit.lower()
    if unit in ['s', 'sec', 'seconds']:
        return value
    elif unit in ['min', 'minutes']:
        return value * 60
    elif unit in ['hour', 'hours']:
        return value * 3600
    elif unit in ['day', 'days']:
        return value * 86400
    elif unit in ['month', 'months']:
        return value * 86400 * 30
    elif unit in ['year', 'years']:
        return value * 86400 * 365
    else:
        return 0


@app.on_message(filters.command("add_premium") & filters.user(EVAL))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 3:
        user_id = message.command[1]
        time_zone = datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p") 
        time = message.command[2]
        user = await client.get_users(user_id)
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.now() + timedelta(seconds=seconds)
            user_data = {"id": int(user.id), "expiry_time": expiry_time}
            await update_user(user_data)
            expiry_str_in_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")         
            await message.reply_text(f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user.id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"👋 ʜᴇʏ {user.mention},\nᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.\nᴇɴᴊᴏʏ !! ✨🎉\n\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True              
            )
        else:
            await message.reply_text("Invalid time format. Please use '1day for days', '1hour for hours', '1min for minutes', '1month for months', or '1year for year'.")
    else:
        await message.reply_text("<b>Usage: /add_premium user_id time\n\nExample: /add_premium 1252789 10days</b>")
        

@app.on_message(filters.command("remove_premium") & filters.user(EVAL))
async def remove_premium_cmd_handler(client, message):
    if len(message.command) == 2:
        user_id = message.command[1]
        user = await client.get_users(user_id)
        user_data = {"id": int(user.id), "expiry_time": None}
        await update_user(user_data)
        await message.reply_text("ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʀᴇᴍᴏᴠᴇᴅ ғᴏʀ ᴛʜᴇ ᴜsᴇʀ !")
        await client.send_message(
            chat_id=user_id,
            text=f"<b>ʜᴇʏ {user.mention},\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.\nᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ ɪғ ᴛʜɪs ɪs ᴀ ᴍɪsᴛᴀᴋᴇ.\n\n👮 ᴏᴡɴᴇʀ: {OWNER_USERNAME}</b>",
            disable_web_page_preview=True
        )
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /remove_premium user_id")


@app.on_message(filters.command("myplan"))
async def check_plans_cmd(client, message):
    user_id = message.from_user.id
    user = message.from_user.mention
    if await has_premium_access(user_id):
        remaining_time = await check_remaining_uasge(user_id)
        expiry_time = datetime.now() + remaining_time
        expiry_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")
        days, seconds = divmod(remaining_time.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes = seconds // 60
        time_left_str = f"{int(days)} ᴅᴀʏꜱ, {int(hours)} ʜᴏᴜʀꜱ, {int(minutes)} ᴍɪɴᴜᴛᴇꜱ"
        await message.reply_text(
            f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n"
            f"👤 ᴜꜱᴇʀ : {user}\n"
            f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
            f"⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n"
            f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}"
        )
    elif message.from_user.id == OWNER_ID:
        await message.reply_text(
            f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n"
            f"👤 ᴜꜱᴇʀ : {user}\n"
            f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
            f"⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : ♾\n"
            f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : ♾"
        )
    else:
        await message.reply_text("**😢 Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ sᴜʙsᴄʀɪᴘᴛɪᴏɴ.**")



@app.on_message(filters.command("premiums") & filters.user(EVAL))
async def premium_users(client, message):
    users = await all_premium_users()
    text = []

    for user in users:
        display_name = None

        if hasattr(user, 'mention'):
            display_name = user.mention
        elif hasattr(user, 'username'):
            display_name = f"@{user.username}"
        elif hasattr(user, 'first_name'):
            display_name = user.first_name
            if hasattr(user, 'last_name'):
                display_name += f" {user.last_name}"
        else:
            display_name = f"User-`{user.id}`"

        if hasattr(user, 'expiry_time'):
            formatted_expiry = user.expiry_time.strftime('%d-%m-%y %H:%M:%S')
            display_name += f" (Expires: {formatted_expiry})"

        text.append(display_name)

    if text:
        await message.reply("\n\n".join(text))
    else:
        await message.reply("No premium users found.")
