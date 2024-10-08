from pyrogram import Client, filters
from pyrogram.types import Message
import io
import re
from EQUROBOT import app

@app.on_message(filters.command(["txt"], [".", "/"]))
async def txt_handler(client, message: Message):
    reply_message = message.reply_to_message.text if message.reply_to_message else None
    
    if reply_message is None:
        await message.reply_text("Please reply to a message with the `.txt` command.")
        return

    processing_message = await message.reply_text("**ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ....💾**")

    document_io = io.BytesIO(reply_message.encode('utf-8'))
    document_io.name = 'cc_clean_card3D.txt'

    await processing_message.delete()

    user = message.from_user
    profile_link = f"https://t.me/{user.username}" if user.username else "No username"
    fullname = user.first_name + (f" {user.last_name}" if user.last_name else "")
    
    await message.reply_document(
        document=document_io,
        caption=(
            "┏━━━━━━➣\n"
            "┣**ʜᴇʀᴇ's ʏᴏᴜʀ .ᴛxᴛ ғɪʟᴇ** ✅\n"
            "┗━━━━━━━━━━━━➣\n"
            f"**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ**: [{fullname}]({profile_link})"
        )
    )

@app.on_message(filters.command(["clean"], [".", "/"]))
async def clean_handler(client, message: Message):
    reply_document = message.reply_to_message.document if message.reply_to_message else None
    
    if reply_document is None:
        await message.reply_text("Please reply to a document file with the `.clean` command.")
        return

    document_path = await client.download_media(reply_document)
    
    with open(document_path, 'r', encoding='utf-8') as file:
        content = file.read()

    sk_pattern = re.compile(r"sk_live_[a-zA-Z0-9]+")
    card_pattern = re.compile(r"(\d{15,16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})")
    proxy_pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}):(\d{2,5})(?::(\w+):(\w+))?")
    
    sk_keys = sk_pattern.findall(content)
    card_details = card_pattern.findall(content)
    proxies = proxy_pattern.findall(content)
    
    if not sk_keys and not card_details and not proxies:
        await message.reply_text("No valid SK keys, card details, or proxies found in the document.")
        return

    cleaned_data = ""
    if sk_keys:
        cleaned_data += "\n".join(sk_keys) + "\n"
    if card_details:
        cleaned_data += "\n".join("|".join(detail) for detail in card_details) + "\n"
    if proxies:
        cleaned_data += "\n".join(
            f"{proxy[0]}:{proxy[1]}" + (f":{proxy[2]}:{proxy[3]}" if proxy[2] and proxy[3] else "")
            for proxy in proxies
        ) + "\n"

    cleaned_document_io = io.BytesIO(cleaned_data.encode('utf-8'))
    cleaned_document_io.name = 'equrobot_cleandb.txt'

    user = message.from_user
    profile_link = f"https://t.me/{user.username}" if user.username else "No username"
    fullname = user.first_name + (f" {user.last_name}" if user.last_name else "")

    sk_indicator = "SK Keys ✅" if sk_keys else ""
    card_indicator = "Cards ✅" if card_details else ""
    proxy_indicator = "Proxies ✅" if proxies else ""
    indicators = f"{sk_indicator}   {card_indicator}   {proxy_indicator}".strip()

    await message.reply_document(
        document=cleaned_document_io,
        caption=(
            f"**ʜᴇʀᴇ's ᴛʜᴇ ᴄʟᴇᴀɴᴇᴅ ғɪʟᴇ** ✅\n"
            f"**{indicators}**\n"
            f"**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ**: [{fullname}]({profile_link})"
        )
    )

@app.on_message(filters.command(["fl"], [".", "/"]))
async def fl_handler(client, message: Message):
    reply_document = message.reply_to_message.document if message.reply_to_message else None
    reply_text = message.reply_to_message.text if message.reply_to_message else None
    
    if not reply_document and not reply_text:
        await message.reply_text("Please reply to a text message or a document with the `.fl` command.")
        return
    
    if reply_document:
        document_path = await client.download_media(reply_document)
        
        with open(document_path, 'r', encoding='utf-8') as file:
            content = file.read()
    else:
        content = reply_text

    sk_pattern = re.compile(r"sk_live_[a-zA-Z0-9]+")
    card_pattern = re.compile(r"(\d{15,16})[|/:](\d{2})[|/:](\d{2,4})[|/:](\d{3,4})")
    proxy_pattern = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3}):(\d{2,5})(?::(\w+):(\w+))?")
    
    sk_keys = sk_pattern.findall(content)[:30]
    card_details = card_pattern.findall(content)[:30]
    proxies = proxy_pattern.findall(content)[:30]
    
    filtered_data = ""
    
    if sk_keys:
        filtered_data += "\n" + "\n".join(f"`{key}`" for key in sk_keys) + "\n"
    
    if card_details:
        filtered_data += "\n" + "\n".join(f"`{'|'.join(detail)}`" for detail in card_details) + "\n"
    
    if proxies:
        filtered_data += "\n" + "\n".join(
            f"`{proxy[0]}:{proxy[1]}" + (f":{proxy[2]}:{proxy[3]}" if proxy[2] and proxy[3] else "") + "`"
            for proxy in proxies
        ) + "\n"
    
    if not filtered_data:
        await message.reply_text("No valid SK keys, card details, or proxies found.")
        return

    await message.reply_text(filtered_data.strip())
        
