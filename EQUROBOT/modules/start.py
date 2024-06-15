from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import BOT_USERNAME, OWNER_ID
from pyrogram.types import InlineKeyboardButton as ib
import asyncio
from EQUROBOT import app


START_TEXT = """
ʜɪ ,

ɪ ᴀᴍ , 
ʏᴏᴜʀ ᴀɪ ᴄᴏᴍᴘᴀɴɪᴏɴ. 
ʟᴇᴛ'ꜱ ᴄʜᴀᴛ ᴀɴᴅ ᴇxᴘʟᴏʀᴇ 
ᴛʜᴇ ᴅᴇᴘᴛʜꜱ ᴏꜰ ᴄᴏɴᴠᴇʀꜱᴀᴛɪᴏɴ ᴛᴏɢᴇᴛʜᴇʀ! 
ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴀꜱᴋ ᴍᴇ ᴀɴʏᴛʜɪɴɢ ᴏʀ ꜱʜᴀʀᴇ ʏᴏᴜʀ ᴛʜᴏᴜɢʜᴛꜱ. 
ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʟɪꜱᴛᴇɴ ᴀɴᴅ ᴇɴɢᴀɢᴇ ɪɴ ᴍᴇᴀɴɪɴɢꜰᴜʟ ᴅɪꜱᴄᴜꜱꜱɪᴏɴꜱ ᴡɪᴛʜ ʏᴏᴜ."
"""



@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    buttons = [
        [
            InlineKeyboardButton("⦿ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ⦿", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
            InlineKeyboardButton("⦿ɢʀᴏᴜᴘ⦿", url=f"https://t.me/CARD3DBOTx"),
            InlineKeyboardButton("⦿ᴏᴡɴᴇʀ⦿", user_id=OWNER_ID)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_video(
        video="https://telegra.ph/file/365de71e032aadb98e1d2.mp4",
        caption=START_TEXT,
        reply_markup=reply_markup
    )
