import os
from pyrogram import Client, filters
import random
import string
from pymongo import MongoClient
from pyrogram.types import Message
from pyrogram.errors import *
from EQUROBOT import app  # Ensure EQUROBOT is defined or import the correct module

# MongoDB connection URL
mongodb_url = 'mongodb+srv://daxxop:daxxop@daxxop.dg3umlc.mongodb.net/?retryWrites=true&w=majority'

# Initialize the MongoDB client
client = MongoClient(mongodb_url)
db = client["api_keys"]

def generate_random_key():
    characters = string.ascii_letters + string.digits + '@#₹_&-+()/*"\':;!?'
    return ''.join(random.choice(characters) for _ in range(30))

def save_api_key(user_id, api_key):
    db.keys.insert_one({"user_id": user_id, "api_key": api_key})

def revoke_api_key(user_id):
    db.keys.delete_one({"user_id": user_id})

def get_user_info(user_id):
    user_data = db.keys.find_one({"user_id": user_id})
    return user_data

@app.on_message(filters.command("api_daxx"))
def api_daxx(client, message: Message):
    random_key = f"DAXX_API{generate_random_key()}"
    user_id = message.from_user.id
    save_api_key(user_id, random_key)
    if message.chat.type == "private":
        message.reply_text(f"𝖸𝖮𝖴𝖱 𝖠𝖯𝖨 𝖪𝖤𝖸 𝖨𝖲:\n `{random_key}`")
    else:
        # Send the API key in a private message if the command is used in a group
        client.send_message(user_id, f"𝖸𝖮𝖴𝖱 𝖠𝖯𝖨 𝖪𝖤𝖸 𝖨𝖲:\n `{random_key}`")
        message.reply_text("𝖠𝖯𝖨 𝖪𝖤𝖸 𝖧𝖠𝖲 𝖡𝖤𝖤𝖭 𝖲𝖤𝖭𝖳 𝖳𝖮 𝖸𝖮𝖴𝖱 𝖣𝖬.")

@app.on_message(filters.command("revoke_api"))
def revoke_api(client, message: Message):
    user_id = message.from_user.id
    revoke_api_key(user_id)
    message.reply_text("𝖠𝖯𝖨 𝖪𝖤𝖸 𝖱𝖤𝖵𝖮𝖪𝖤𝖣 𝖲𝖴𝖢𝖢𝖤𝖲𝖲𝖥𝖴𝖫𝖫𝖸.")

@app.on_message(filters.command("info"))
def user_info(client, message: Message):
    user_id = message.from_user.id
    user_data = get_user_info(user_id)
    if user_data:
        api_key = user_data["api_key"]
        message.reply_text(f"𝖴𝖲𝖤𝖱 𝖨𝖣: `{user_id}`\n\n 𝖸𝖮𝖴𝖱 𝖠𝖯𝖨 𝖪𝖤𝖸 𝖨𝖲: `{api_key}`")
    else:
        message.reply_text("𝖭𝖮 𝖠𝖯𝖨 𝖪𝖤𝖸 𝖥𝖮𝖴𝖭𝖣. 𝖦𝖤𝖭𝖤𝖱𝖠𝖳𝖤 𝖮𝖭𝖤 𝖴𝖲𝖨𝖓𝖌 /api_daxx")
        
