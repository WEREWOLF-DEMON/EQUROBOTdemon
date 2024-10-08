from EQUROBOT import app
from pymongo import MongoClient
import hashlib
import random
import string
from pyrogram import filters

client = MongoClient('mongodb+srv://git:git@git.scvzxhw.mongodb.net')
db = client.mohio
collection = db.mohio

user_data = {}

def generate_invite_code():
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return "GITWIZARD" + random_string

@app.on_message(filters.command(["login"]))
async def login(_, message):
    try:
        username_msg = await message.reply_text("✅ **ENTER YOUR USERNAME**")
        input = await app.listen(user_id=message.from_user.id)
        username = input.text
        await input.delete()

        user = collection.find_one({"username": username})
        if not user:
            return await message.reply_text("❌ Username Not Found in Database \n\n Register First at z.daxxteam.com")

        password_msg = await message.reply_text("✅ **ENTER YOUR PASSWORD**")
        input0 = await app.listen(user_id=message.from_user.id)
        password = input0.text
        await input0.delete()

        if user['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
            user_data[message.from_user.id] = {'username': username, 'password': password}
            await message.reply_text("✅ **Login Successful!**")
        else:
            await message.reply_text("❌ **Login Failed!**\n\nReason: `Password Incorrect`")
    except Exception as e:
        print(e)
        await message.reply_text(f"❌ **Login Failed**\n\nReason: {e}")

@app.on_message(filters.command(["fingerprint"]))
async def fingerprint(_, message):
    try:
        user_info = user_data.get(message.from_user.id)
        if not user_info:
            return await message.reply_text("❌ **Login Required**\n\nPlease login first to use this command.")

        username = user_info.get('username')
        password = user_info.get('password')

        user = collection.find_one({"username": username, "password": hashlib.sha256(password.encode('utf-8')).hexdigest()})
        if not user:
            return await message.reply_text("❌ **User Not Found in Database**")

        if len(message.text.split()) > 1:
            fingerprint = message.text.split(" ", 1)[1]
            collection.update_one({"username": username}, {"$push": {"fingerprint": int(fingerprint)}})
            await message.reply_text(f"✅ **Fingerprint Updated to `{fingerprint}`**")
        else:
            fingerprint_list = user.get('fingerprint', [])
            fingerprint_list = [str(fp) for fp in fingerprint_list]
            if fingerprint_list:
                fingerprints = ', '.join(fingerprint_list)
                await message.reply_text(f"**Your Fingerprints:** `{fingerprints}`\n\nTo add a new fingerprint, provide it after the /fingerprint command.")
            else:
                await message.reply_text("❌ **No Fingerprints Set Yet**\n\nTo add a new fingerprint, provide it after the /fingerprint command.")
    except Exception as e:
        print(e)
        await message.reply_text(f"❌ **Failed to Update Fingerprint**\n\nReason: {e}")

@app.on_message(filters.command(["invite"]))
async def generate_invite(_, message):
    try:
        user_info = user_data.get(message.from_user.id)
        if not user_info:
            return await message.reply_text("❌ **Login Required**\n\nPlease login first to use this command.")

        if len(message.command) < 2:
            return await message.reply_text("❌ **Invalid Command Usage**\n\nUsage: /invite @username")

        target_username = message.command[1]
        user = collection.find_one({"username": user_info.get('username')})
        if not user or user['role'] != 'admin':
            return await message.reply_text("❌ **You do not have permission to generate invite codes.**")

        invite_code = generate_invite_code()
        collection.update_one({"username": user_info.get('username')}, {"$set": {"invites." + invite_code: {"is_used": False, "who_used": ""}}})

        try:
            await app.send_message(target_username, f"✅ **Invite Code Generated:** `{invite_code}`")
            await message.reply_text(f"✅ **Invite Code Sent to {target_username}**")
        except Exception as e:
            await message.reply_text(f"❌ **Failed to Send Invite Code to {target_username}**\n\nReason: {e}")
    except Exception as e:
        print(e)
        await message.reply_text(f"❌ **Failed to Generate Invite Code**\n\nReason: {e}")

@app.on_message(filters.command(["revoke_invites"]))
async def revoke_invites(_, message):
    try:
        user_info = user_data.get(message.from_user.id)
        if not user_info:
            return await message.reply_text("❌ **Login Required**\n\nPlease login first to use this command.")

        username = user_info.get('username')
        user = collection.find_one({"username": username})
        if not user or user['role'] != 'admin':
            return await message.reply_text("❌ **You do not have permission to revoke invite codes.**")

        collection.update_many({}, {"$unset": {"invites": ""}})
        await message.reply_text("✅ **All Invite Codes Revoked**")
    except Exception as e:
        print(e)
        await message.reply_text(f"❌ **Failed to Revoke Invite Codes**\n\nReason: {e}")
