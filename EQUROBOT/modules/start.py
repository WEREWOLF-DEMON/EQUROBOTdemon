from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.enums import ChatType
import asyncio
import os
from os import getenv
import traceback
from pyrogram import filters, Client
from pyrogram.types import Message
from unidecode import unidecode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import random 
import time
import random
from EQUROBOT import app as Client
from config import BOT_USERNAME, OWNER_ID


AM_PIC = [
    "https://telegra.ph/file/365de71e032aadb98e1d2.mp4",
    "https://telegra.ph/file/365de71e032aadb98e1d2.mp4",
    
]
ban_txt = """
ʜɪ {} ,
ɪ ᴀᴍ , 
ʏᴏᴜʀ ᴀɪ ᴄᴏᴍᴘᴀɴɪᴏɴ. 
ʟᴇᴛ'ꜱ ᴄʜᴀᴛ ᴀɴᴅ ᴇxᴘʟᴏʀᴇ 
ᴛʜᴇ ᴅᴇᴘᴛʜꜱ ᴏꜰ ᴄᴏɴᴠᴇʀꜱᴀᴛɪᴏɴ ᴛᴏɢᴇᴛʜᴇʀ! 
ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴀꜱᴋ ᴍᴇ ᴀɴʏᴛʜɪɴɢ ᴏʀ ꜱʜᴀʀᴇ ʏᴏᴜʀ ᴛʜᴏᴜɢʜᴛꜱ. 
ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʟɪꜱᴛᴇɴ ᴀɴᴅ ᴇɴɢᴀɢᴇ ɪɴ ᴍᴇᴀɴɪɴɢꜰᴜʟ ᴅɪꜱᴄᴜꜱꜱɪᴏɴꜱ ᴡɪᴛʜ ʏᴏᴜ.
"""
help_txt = """
» ʙᴏᴛ ғᴇᴀᴛᴜʀᴇs.
"""
killall_txt = """
1. <code>/start</code> - start bot

ɴᴏᴡ ʙᴏᴛ ᴡɪʟʟ ᴡᴏʀᴋɪɴɢ ɪɴ ɢʀᴏᴜᴘ ✅.
"""
Rbanall = """
1. <code>/start</code> - start bot

ɴᴏᴡ ʙᴏᴛ ᴡɪʟʟ ᴡᴏʀᴋɪɴɢ ɪɴ ɢʀᴏᴜᴘ ✅.

ɴᴏᴛᴇ : ᴛʜɪꜱ ᴄᴍᴅꜱ ᴏɴʟʏ ᴡᴏʀᴋ ɪɴ ʙᴏᴛ ᴘᴍ.
"""

gate_txt = f"""
gates here
"""

auth_txt = f"""
chk here

"""

app_buttons = [

                [ 
                    InlineKeyboardButton("tools", callback_data="banall_"),
                    InlineKeyboardButton("checker", callback_data="rbanall_"),
        
                ],
                [ 
                    InlineKeyboardButton("auth chk", callback_data="auth_"),
                    InlineKeyboardButton("auth gate", callback_data="gate_"),
        
                ],
                [
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="home_"),
                    InlineKeyboardButton("⟲ ᴄʟᴏꜱᴇ ⟳", callback_data="close_data")
                ]
                ]

back_buttons  = [[
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="help_"),                    
                ]]

button = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⦿ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ⦿", url=f"https://t.me/{app.me.username}?startgroup=true")
        ],
        [
            InlineKeyboardButton("⦿ɢʀᴏᴜᴘ⦿", url=f"https://t.me/ALLTYPECC"),    
        ],
       [
            InlineKeyboardButton("⦿ ᴏᴡɴᴇʀ ⦿", user_id=OWNER_ID)  
        ],
    [
           InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_"),    
      ]
    
])

@Client.on_message(filters.command(["start"], prefixes=[".","/","!"]) & filters.private)
async def start(_, message):
    await message.reply_video(
        video=random.choice(AM_PIC),
        caption=ban_txt.format(message.from_user.mention, message.from_user.id, app.me.username),
        reply_markup=button
    )    

@Client.on_callback_query()
async def cb_handler(client, query):
    if query.data=="home_":
        buttons =  [
            [
            InlineKeyboardButton("⦿ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ⦿", url=f"https://t.me/{app.me.username}?startgroup=true")
        ],
            [
            InlineKeyboardButton("⦿ɢʀᴏᴜᴘ⦿", url=f"https://t.me/ALLTYPECC"),    
        ],
            [
            InlineKeyboardButton("⦿ ᴏᴡɴᴇʀ ⦿", user_id=OWNER_ID)  
        ],
            [
                InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_")
            ]    
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                ban_txt.format(query.from_user.mention, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="help_":        
        reply_markup = InlineKeyboardMarkup(app_buttons)
        try:
            await query.edit_message_text(
                help_txt,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass



    elif query.data=="banall_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                killall_txt,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="rbanall_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                Rbanall,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    
    elif query.data=="auth_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                auth_txt,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    
    elif query.data=="gate_":        
        reply_markup = InlineKeyboardMarkup(back_buttons)
        try:
            await query.edit_message_text(
                gate_txt,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass
  
    elif query.data=="close_data":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass
