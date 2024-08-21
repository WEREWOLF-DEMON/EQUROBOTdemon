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
from EQUROBOT import app
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
EQUROBOT Tools
━━━━━━━━━━━━━━━
𝟣. 𝖨𝖯 𝖫𝗈𝗈𝗄𝗎𝗉
    ➜ 𝖢𝖬𝖣: /ip your_ip
    ➜ 𝖢𝖬𝖣: /ipgen fake ip

𝟤. 𝖢𝖢 𝖲𝖼𝗋𝖺𝗉𝖾𝗋
    ➜ 𝖢𝖬𝖣: /scr channel_username 100

𝟥. 𝖯𝗋𝗈𝗑𝗒 𝖢𝗁𝖾𝖼𝗄𝖾𝗋
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /proxy your_proxy

𝟦. 𝖦𝖺𝗍𝖾𝗐𝖺𝗒 𝖧𝗎𝗇𝗍𝖾𝗋
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /gate website_url

𝟧. 𝖬𝗈𝗇𝗀𝗈𝖽𝖻 𝖢𝗁𝖾𝖼𝗄𝖾𝗋
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /mongochk

𝟨. 𝖣𝗎𝗆𝗉
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /dump

𝟩. 𝖶𝖾𝖻𝗌𝗂𝗍𝖾 𝖨𝗇𝖿𝗈𝗋𝗆𝖺𝗍𝗂𝗈𝗇
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /domain


𝟪. 𝖦𝗈𝗈𝗀𝗅𝖾 𝖣𝗈𝗋𝗄 𝖱𝖾𝗌𝗎𝗅𝗍𝗌
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /dork

𝟫. 𝖦𝗂𝗍𝖧𝗎𝖻 𝖨𝗇𝖿𝗈𝗋𝗆𝖺𝗍𝗂𝗈𝗇
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /git GitHub username
    
𝖳𝗈𝗍𝖺𝗅 𝖳𝗈𝗈𝗅𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌: 𝟪

"""
Rbanall = """
EQUROBOT Checker
━━━━━━━━━━━━━━━
𝟣. 𝖡𝖨𝖭 𝗂𝗇𝖿𝗈 𝖢𝗁𝖾𝖼𝗄𝖾𝗋
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾:   /bin 440393

𝟤. 𝖱𝖺𝗇𝖽𝗈𝗆 𝖢𝖢 𝖦𝖾𝗇𝖺𝗋𝖺𝗍𝗈𝗋
    ➜ 𝖢𝖬𝖣:   /gen 440393 500

𝟥. 𝖢𝖢 𝗂𝗇𝖿𝗈 𝖢𝗁𝖾𝖼𝗄𝖾𝗋
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾:  /chk cc|mm|yy|cvv

𝟦. 𝖵𝖡𝖵 𝖫𝗈𝗈𝗄𝗎𝗉
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾:  /vbv cc|mm|yy|cvv 

𝟧. 𝖥𝖺𝗄𝖾 𝖢𝗈𝗎𝗇𝗍𝗋𝗒 𝖠𝖽𝖽𝗋𝖾𝗌𝗌
    ➜ 𝖢𝖬𝖣: /fake us
   
𝟨. 𝖲𝗄 𝗄𝖾𝗒 𝖢𝗁𝖾𝖼𝗄
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /sk sk_live_EquRobot

   𝖳𝗈𝗍𝖺𝗅 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌: 𝟨
   
"""

gate_txt = f"""
EQUROBOT Bot Tools
━━━━━━━━━━━━━━━
𝟣. 𝖪𝗇𝗈𝗐 𝖸𝗈𝗎𝗋 𝖴𝗌𝖾𝗋 𝖨𝖣
   𝖢𝖬𝖣: /id

𝟤. 𝖪𝗇𝗈𝗐 𝖸𝗈𝗎𝗋 𝖥𝗎𝗅𝗅 𝗂𝗇𝖿𝗈 𝗈𝗇 𝖮𝗎𝗋 𝖡𝗈𝗍
   𝖢𝖬𝖣: /info

𝟥 . 𝖦𝗂𝗍𝗐𝗂𝗓𝖺𝗋𝖽 𝖫𝗈𝗀𝗂𝗇
    𝖢𝖬𝖣: /login

𝟦 .𝖠𝗇𝗂𝗆𝖾
    ➜ 𝖲𝗂𝗇𝗀𝗅𝖾:  /anime

𝟧 . 𝖲𝖼𝗋𝖾𝖾𝗇𝖲𝗁𝗈𝗍
     ➜ 𝖲𝗂𝗇𝗀𝗅𝖾:  /ss

𝟨 . 𝖴𝗉𝗌𝖼𝖺𝗅𝖾   
     ➜ 𝖲𝗂𝗇𝗀𝗅𝖾:  /upscale 

𝟩 . 𝖣𝗋𝖺𝗐
     ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /draw

𝟪 . 𝖸𝖳 𝖲𝗈𝗇𝗀𝗌 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽
     ➜ 𝖲𝗂𝗇𝗀𝗅𝖾: /song


𝟫 . 𝖨𝗇𝗌𝗍𝖺 𝖱𝖾𝖾𝗅𝗌 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽
     ➜ 𝖲𝗂𝗇𝗀𝗅𝖾:  /ig [ 𝘙𝘦𝘦𝘭 𝘓𝘪𝘯𝘬 ]


𝟣𝟢 . 𝖡𝗎𝗀𝗌
      ➜ 𝖲𝗂𝗇𝗀𝗅𝖾:  /bugs [ 𝘚𝘦𝘯𝘥 𝘠𝘰𝘶𝘳 𝘗𝘳𝘰𝘣𝘭𝘦𝘮 ]

   𝖳𝗈𝗍𝖺𝗅 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌: 10   
"""

auth_txt = f"""
𝖠𝗂 𝖳𝗈𝗈𝗅𝗌 𝖮𝖿 EQUROBOT
━━━━━━━━━━━━━━━
𝟣. 𝖢𝗁𝖺𝗍𝖦𝖯𝖳
    ➜ 𝖢𝖬𝖣: /gpt [ in reply to text ]
    ➜ 𝖢𝖬𝖣: /gpt your_prompt

𝟤. EQUROBOT AI
    ➜ 𝖢𝖬𝖣: /equ [ in reply to text ]

𝟥. 𝖳𝖾𝗑𝗍 𝗍𝗈 𝖲𝗉𝖾𝖾𝖼𝗁 (𝖳𝖳𝖲)
    ➜ 𝖢𝖬𝖣: /siri your_text

𝖳𝗈𝗍𝖺𝗅 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌: 4

"""

app_buttons = [

                [ 
                    InlineKeyboardButton("𝖳𝗈𝗈𝗅𝗌", callback_data="banall_"),
                    InlineKeyboardButton("𝖢𝗁𝖾𝖼𝗄𝖾𝗋", callback_data="rbanall_"),
        
                ],
                [ 
                    InlineKeyboardButton("𝖠𝗂", callback_data="auth_"),
                    InlineKeyboardButton("𝖡𝗈𝗍", callback_data="gate_"),
        
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
            InlineKeyboardButton("⦿ɢʀᴏᴜᴘ⦿", url=f"https://t.me/StdBotz"),  
            InlineKeyboardButton("⦿ ᴏᴡɴᴇʀ ⦿", user_id=OWNER_ID)  
        ],
    [
           InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_"),    
      ]
    
])

@app.on_message(filters.command(["start"], prefixes=[".","/","!"]) & filters.private)
async def start(_, message):
    await message.reply_video(
        video=random.choice(AM_PIC),
        caption=ban_txt.format(message.from_user.mention, message.from_user.id, app.me.username),
        reply_markup=button
    )    

@app.on_callback_query()
async def cb_handler(client, query):
    if query.data=="home_":
        buttons =  [
            [
            InlineKeyboardButton("⦿ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ⦿", url=f"https://t.me/{app.me.username}?startgroup=true")
        ],
            [
            InlineKeyboardButton("⦿ɢʀᴏᴜᴘ⦿", url=f"https://t.me/ALLTYPECC"),    
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
