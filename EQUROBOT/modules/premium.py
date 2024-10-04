import asyncio
import time
from pyrogram import Client, filters
from pymongo import MongoClient
from EQUROBOT import app
from config import OWNER_ID, CLONEDB

mongo_uri = CLONEDB

client = MongoClient(mongo_uri)
db = client["telegram_bot"]
premium_collection = db["premium_users"]

owner_user_id = OWNER_ID

def parse_time(time_str):
    time_in_seconds = 0
    units = {'m': 60, 'h': 3600, 'd': 86400, 'w': 604800}
    
    num = ''
    for char in time_str:
        if char.isdigit():
            num += char
        elif char in units:
            if num:
                time_in_seconds += int(num) * units[char]
                num = ''
    
    return time_in_seconds

@app.on_message(filters.command("add"))
async def add_premium(client, message):
    user_id = message.from_user.id
    
    if user_id != owner_user_id:
        await message.reply("You don't have permission to use this command.")
        return
    
    try:
        _, user_id_str, *time_parts = message.text.split()
        user_id_to_add = int(user_id_str)
        time_str = ''.join(time_parts)
        duration_seconds = parse_time(time_str)
        expiration_time = time.time() + duration_seconds

        premium_collection.update_one(
            {"user_id": user_id_to_add},
            {"$set": {"expiration_time": expiration_time}},
            upsert=True
        )

        await message.reply(f"User {user_id_to_add} has been added as a premium user for {time_str}.")
    
    except ValueError:
        await message.reply("Invalid command format. Use /add userID duration (e.g., /add 123456789 1m 1h 1w).")

@app.on_message(filters.command("total"))
async def total_users(client, message):
    user_id = message.from_user.id
    
    if user_id != owner_user_id:
        await message.reply("You don't have permission to use this command.")
        return
    
    total_premium = premium_collection.count_documents({})
    await message.reply(f"Total Premium Users: {total_premium}")

@app.on_message(filters.command("remove"))
async def remove_user(client, message):
    user_id = message.from_user.id
    
    if user_id != owner_user_id:
        await message.reply("You don't have permission to use this command.")
        return
    
    try:
        _, user_id_str = message.text.split()
        user_id_to_remove = int(user_id_str)

        result = premium_collection.delete_one({"user_id": user_id_to_remove})
        
        if result.deleted_count:
            await message.reply(f"User {user_id_to_remove} has been removed from premium.")
        else:
            await message.reply(f"User {user_id_to_remove} was not found in the premium list.")
    
    except ValueError:
        await message.reply("Invalid command format. Use /remove userID (e.g., /remove 123456789).")

@app.on_message(filters.command("removeall"))
async def remove_all_users(client, message):
    user_id = message.from_user.id
    
    if user_id != owner_user_id:
        await message.reply("You don't have permission to use this command.")
        return
    
    premium_collection.delete_many({})
    await message.reply("All premium users have been removed.")
  
