import logging
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram.filters import create
from pyrogram.enums import MessageEntityType, ParseMode
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from pyrogram.errors import AccessTokenExpired, AccessTokenInvalid
from config import API_ID, API_HASH, LOGGER_ID, OWNER_ID
from EQUROBOT import app

MONGO_DB = 'mongodb+srv://piyush2004:piyush2004@cluster0.7w3eadf.mongodb.net'

CLONES = set()

mongo = MongoCli(MONGO_DB)
db = mongo.EQUROBOT
clonebotdb = db.clonebotdb

async def start_bot(bot_token):
    try:
        ai = Client(
            name=f"clone_{bot_token}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=bot_token,
            plugins=dict(root="EQUROBOT.Clone")
        )
        await ai.start()
        bot_info = await ai.get_me()
        commands = [
            BotCommand("start", "Just start and see the result 😉")
        ]
        await ai.set_bot_commands(commands)

        return bot_info
    except Exception as e:
        logging.exception(f"Error while starting bot with token {bot_token}")
        return None


@app.on_message(filters.command(["clone", "host", "deploy"]))
async def clone(client, message):
    await message.reply_text("""
🤖 **To create a EQUROBOT Bot clone, follow these simple steps:**

1. Go to **@BotFather**
2. Start it and press **/newbot**
3. Write the **Name** of the bot
4. Write the **username** of the bot
5. **Forward** (don't copy-paste) here the message that you'll receive from BotFather.
6. **Done!**

**To disconnect it from server use /mybot**
""")

forwarded_from_botfather = create(lambda _, client, message: message.forward_from and message.forward_from.username.lower() == "botfather")

def extract_bot_token(msg_text, entities):
    for entity in entities:
        if entity.type == MessageEntityType.CODE:
            return msg_text[entity.offset:entity.offset + entity.length]


@app.on_message(forwarded_from_botfather & filters.private)
async def clone_bot(client, message):
    entities = message.entities
    msg_text = message.text or ""
    bot_token = extract_bot_token(msg_text, entities)

    mi = await message.reply_text("Generating a clone.. Please wait..")
    
    cloned_bot = await clonebotdb.find_one({"token": bot_token})
    if cloned_bot:
        await mi.edit_text("**🤖 Your bot is already cloned ✅**")
        return

    cbot = await clonebotdb.find_one({"user_id": message.from_user.id})
    if cbot :
        await mi.edit_text("**🤖 Your can clone 1 bot only**")
        return

    try:
        bot = await start_bot(bot_token)
    except Exception as e:
        logging.exception("Exception occurred during token validation.")
        await mi.edit_text(f"**Error while checking bot token:** {e}")
        return

    await mi.edit_text("**Cloning process started. Please wait...**")
    try:
        owner = message.from_user
        await app.send_message(
            int(LOGGER_ID), 
            f"**#New_Clone**\n\n"
            f"**Bot:** @{bot.username}\n"
            f"**Bot ID:** `{bot.id}`\n"
            f"**Bot Token:** `{bot_token}`\n"
            f"**Owner ID:** `{owner.id}`\n"
            f"**Owner Mention:** {owner.mention or owner.username}\n"
            f"**Owner Full Name:** {owner.first_name} {owner.last_name or ''}"
        )

        details = {
            "bot_id": bot.id,
            "is_bot": True,
            "user_id": message.from_user.id,
            "name": bot.first_name,
            "token": bot_token,
            "username": bot.username,
        }
        await clonebotdb.insert_one(details)
        CLONES.add(bot.id)
        await mi.edit_text(f"**Bot @{bot.username} has been successfully cloned and started ✅.**\n**See:** /mybot")
    except Exception as e:
        logging.exception("Error while cloning bot.")
        await mi.edit_text(f"⚠️ **Error:**\n\n`{e}`\n\n**Kindly forward this message to @Mohitag403_bot for assistance**")



@app.on_message(filters.command(["mybot"]))
async def delete_cloned_bot(client, message):
    join = await subscribe(client, message, message.from_user.id)
    if join ==1:
        return
    try:
        bot = await clonebotdb.find_one({"user_id": message.from_user.id})
        if bot:
            bot_token = bot["token"]
            bot_username = bot["username"]
            reply_text = f"**Your Bot: @{bot_username} \n\nBot Token:** `{bot_token}`"

            button1 = InlineKeyboardButton("Delete Bot", callback_data="delete")
            button2 = InlineKeyboardButton("Close", callback_data="close")
            keyboard = InlineKeyboardMarkup([[button1], [button2]])
            
            m = await message.reply_text(reply_text, reply_markup=keyboard)
            r = await m.wait_for_click(from_user_id=message.from_user.id)
            
            if r.data == "delete":
                await clonebotdb.delete_one({"_id": bot["_id"]})
                CLONES.discard(bot["bot_id"])
                await m.edit_text("**🤖 Your cloned bot has been disconnected from my server ☠️**\n**Reclone by:** /clone")
                os.system(f"kill -9 {os.getpid()} && bash start")
            elif r.data == "close":
                await m.delete()
        else:
            await message.reply_text("**You have not cloned any bot clone by /clone**")
    except Exception as e:
        logging.exception("Error while deleting cloned bot.")
        await message.reply_text(f"**An error occurred while deleting the cloned bot:** {e}")



@app.on_message(filters.command("delallclone") & filters.user(OWNER_ID))
async def delete_all_cloned_bots(client, message):
    a = await message.reply_text("**Deleting all cloned bots...**")
    try:
        cloned_bots = await clonebotdb.find().to_list(length=None)
        if not cloned_bots:
            await a.edit_text("**No cloned bots to delete.**")
            return
        
        await clonebotdb.delete_many({})
        CLONES.clear()

        os.system(f"kill -9 {os.getpid()} && bash start")
        await a.edit_text("**All cloned bots have been deleted successfully ✅**")
    except Exception as e:
        logging.exception("Error while deleting all cloned bots.")
        await a.edit_text(f"**An error occurred while deleting all cloned bots:** {e}")


async def restart_bots():
    global CLONES
    try:
        logging.info("Restarting all cloned bots...")
        tasks = []
        
        async for bot in clonebotdb.find():
            bot_token = bot["token"]
            user_id = bot["user_id"]
            tasks.append(start_bot_with_check(bot_token))
        
        results = await asyncio.gather(*tasks)
        for bot_id in results:
            if bot_id is not None:
                CLONES.add(bot_id)
        await app.send_message(LOGGER_ID, "𝐀𝐋𝐋 𝐂𝐋𝐎𝐍𝐄𝐃 𝐁𝐎𝐓𝐒 𝐒𝐓𝐀𝐑𝐓𝐄𝐃........⚡️⚡️")
    except Exception as e:
        logging.exception("Error while restarting bots.")


async def start_bot_with_check(bot_token):
    try:
        bot = await start_bot(bot_token)
        return bot.id
    except (AccessTokenExpired, AccessTokenInvalid):
        logging.warning(f"Bot token {bot_token} is invalid or expired.")
        await clonebotdb.delete_one({"token": bot_token})
        return None
    except Exception as e:
        logging.exception(f"Unexpected error starting bot with token {bot_token}: {e}")
        await clonebotdb.delete_one({"token": bot_token})
        return None


@app.on_message(filters.command("cloned") & filters.user(OWNER_ID))
async def list_cloned_bots(client, message):
    try:
        cloned_bots_list = await clonebotdb.find().to_list(length=None)

        if not cloned_bots_list:
            await message.reply_text("No bots have been cloned yet.")
            return

        total_clones = len(cloned_bots_list)
        caption = f"**✅ Total Cloned Bots:** {total_clones}\n\n"

        async def get_user_info(user_id):
            try:
                return await client.get_users(user_id)
            except Exception:
                return None

        tasks = [get_user_info(bot['user_id']) for bot in cloned_bots_list]
        users = await asyncio.gather(*tasks)

        text = ""
        for no, (bot, user) in enumerate(zip(cloned_bots_list, users), start=1):
            text += f"{no}. Bot ID: {bot['bot_id']}\n"
            text += f"   Bot Name: {bot['name']} (@{bot['username']})\n"
            text += f"   Owner ID: {bot['user_id']}\n"

            if user:
                owner_name = user.first_name + (f" {user.last_name}" if user.last_name else "")
                text += f"   Owner {'Username: @' + user.username + ' (Name: ' + owner_name + ')' if user.username else 'Name: ' + owner_name}\n"

            text += f"   Bot Token: {bot['token']}\n\n"

        with open('Cloned.txt', 'w') as f:
            f.write(text)

        await message.reply_document('Cloned.txt', caption=caption)
        os.remove('Cloned.txt')
    except Exception as e:
        logging.exception("Error while listing cloned bots.")
        await message.reply_text("**An error occurred while listing cloned bots.**")
