import re
import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import AccessTokenExpired, AccessTokenInvalid
from motor.motor_asyncio import AsyncIOMotorClient
from config import API_ID, API_HASH, OWNER_ID, CLONEDB
from EQUROBOT import app
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

LOGGER_ID = -1002237336934
CLONE_LOGS = -1002237336934
PCLONE_LOGS = -1002237336934


try:
    _mongo_async_ = AsyncIOMotorClient(CLONEDB)
    mongodb = _mongo_async_.clonebot
    clonebotsdb = mongodb.clonebots
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")

# Set to keep track of clones
CLONES = set()

async def start_bot(bot_token):
    try:
        ai = Client(
            name=f"clone_{bot_token}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=bot_token,
            plugins=dict(root="CloneBoT.Clones")
        )
        await ai.start()
        bot_info = await ai.get_me()
        commands = [BotCommand("start", "Just start and see the result 😉")]
        await ai.set_bot_commands(commands)
        return bot_info
    except Exception as e:
        logging.error(f"Error while starting bot with token {bot_token}: {e}")
        return None

@app.on_message(filters.command(["clone", "host", "deploy"]))
async def clone(client, message):
    await message.reply_text("""
🤖 To create an unacademy bot clone, follow these simple steps:
1. Go to @BotFather
2. Start it and press /newbot
3. Write the name of the bot
4. Write the username of the bot
5. Forward (don't copy-paste) here the message that you'll receive from BotFather.
6. Done!
Use /mybot to disconnect it from the server.
""")

forwarded_from_botfather = filters.create(lambda _, __, message: message.forward_from and message.forward_from.username.lower() == "botfather")

def extract_bot_token(msg_text, entities):
    for entity in entities:
        if entity.type == MessageEntityType.CODE:
            return msg_text[entity.offset:entity.offset + entity.length]
    return None

@app.on_message(forwarded_from_botfather & filters.private)
async def clone_bot(client, message):
    entities = message.entities
    msg_text = message.text or ""
    bot_token = extract_bot_token(msg_text, entities)
    
    if not bot_token:
        await message.reply_text("Invalid token. Please forward the correct message from BotFather.")
        return

    mi = await message.reply_text("Generating a clone.. please wait..")
    
    if await clonebotsdb.find_one({"token": bot_token}):
        await mi.edit_text("🤖 Your bot is already cloned ✅")
        return

    if await clonebotsdb.find_one({"user_id": message.from_user.id}):
        await mi.edit_text("🤖 You can only clone one bot.")
        return

    bot = await start_bot(bot_token)
    if not bot:
        await mi.edit_text("Error while starting the bot. Please check the bot token.")
        return

    await mi.edit_text("Cloning process started. Please wait...")
    try:
        owner = message.from_user
        log_message = (
            f"#New_Clone\n\n"
            f"Bot Username: @{bot.username}\n"
            f"Bot ID: <code>{bot.id}</code>\n"
            f"Bot Token: <code>{bot_token}</code>\n"
            f"Bot Owner ID: <code>{owner.id}</code>\n"
            f"Bot Owner Mention: {owner.mention or owner.username}\n"
            f"Bot Owner Full Name: {owner.first_name} {owner.last_name or ''}"
        )
        await app.send_message(CLONE_LOGS, log_message)
        await app.send_message(PCLONE_LOGS, log_message)

        details = {
            "bot_id": bot.id,
            "is_bot": True,
            "user_id": message.from_user.id,
            "name": bot.first_name,
            "token": bot_token,
            "username": bot.username,
        }
        await clonebotsdb.insert_one(details)
        CLONES.add(bot.id)
        await mi.edit_text(f"Bot @{bot.username} has been successfully cloned and started ✅.\nSee: /mybot")
    except Exception as e:
        logging.error(f"Error while cloning bot: {e}")
        await mi.edit_text(f"⚠️ Error:\n\n<code>{e}</code>\n\nKindly forward this message to @ItsAMBOTs for assistance.")

@app.on_message(filters.command(["mybot"]))
async def delete_cloned_bot(client, message):
    try:
        bot = await clonebotsdb.find_one({"user_id": message.from_user.id})
        if not bot:
            await message.reply_text("You have not cloned any bot. Use /clone.")
            return

        bot_token = bot["token"]
        bot_username = bot["username"]
        reply_text = f"Your bot: @{bot_username} \n\nBot Token: <code>{bot_token}</code>"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Delete Clone", callback_data="delete")],
            [InlineKeyboardButton("❌", callback_data="close")]
        ])
        m = await message.reply_text(reply_text, reply_markup=keyboard)
        r = await m.wait_for_click(from_user_id=message.from_user.id)
        
        if r.data == "delete":
            await clonebotsdb.delete_one({"_id": bot["_id"]})
            CLONES.discard(bot["bot_id"])
            await m.edit_text("🤖 Your cloned bot has been deleted from my server ☠️\nReclone with: /clone")
            os.system(f"kill -9 {os.getpid()} && bash start")
        elif r.data == "close":
            await m.delete()
    except Exception as e:
        logging.error(f"Error while deleting cloned bot: {e}")
        await message.reply_text(f"An error occurred while deleting the cloned bot: {e}")

@app.on_message(filters.command("delallclone") & filters.user(OWNER_ID))
async def delete_all_cloned_bots(client, message):
    a = await message.reply_text("Deleting all cloned bots...")
    try:
        if not await clonebotsdb.count_documents({}):
            await a.edit_text("No cloned bots to delete.")
            return
        
        await clonebotsdb.delete_many({})
        CLONES.clear()
        os.system(f"kill -9 {os.getpid()} && bash start")
        await a.edit_text("All cloned bots have been deleted successfully ✅")
    except Exception as e:
        logging.error(f"Error while deleting all cloned bots: {e}")
        await a.edit_text(f"An error occurred while deleting all cloned bots: {e}")

async def restart_bots():
    global CLONES
    try:
        logging.info("Restarting all cloned bots...")
        tasks = [start_bot_with_check(bot["token"]) for bot in await clonebotsdb.find().to_list(length=None)]
        results = await asyncio.gather(*tasks)
        CLONES.update(filter(None, results))
    except Exception as e:
        logging.error(f"Error while restarting bots: {e}")

async def start_bot_with_check(bot_token):
    try:
        bot = await start_bot(bot_token)
        return bot.id
    except (AccessTokenExpired, AccessTokenInvalid):
        logging.warning(f"Bot token {bot_token} is invalid or expired.")
        await clonebotsdb.delete_one({"token": bot_token})
        return None
    except Exception as e:
        logging.error(f"Unexpected error starting bot with token {bot_token}: {e}")
        await clonebotsdb.delete_one({"token": bot_token})
        return None

async def send_message_chunks(chat_id, message, chunk_size=4000):
    chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]
    for chunk in chunks:
        await app.send_message(chat_id, chunk)

@app.on_message(filters.command("cloned") & filters.user(OWNER_ID))
async def list_cloned_bots(client, message):
    try:
        cloned_bots_list = await clonebotsdb.find().to_list(length=None)
        if not cloned_bots_list:
            await message.reply_text("No bots have been cloned yet.")
            return

        total_clones = len(cloned_bots_list)
        text = f"Total cloned bots: {total_clones}\n\n"
        for bot in cloned_bots_list:
            text += (
                f"Bot ID: <code>{bot['bot_id']}</code>\n"
                f"Bot Name: {bot['name']}\n"
                f"Bot Username: @{bot['username']}\n\n"
            )
        await send_message_chunks(message.chat.id, text)
    except Exception as e:
        logging.error(f"Error while listing cloned bots: {e}")
        await message.reply_text("An error occurred while listing cloned bots.")
