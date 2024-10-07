from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from datetime import datetime, timedelta
from EQUROBOT import app
import asyncio
from config import OWNER_ID

mongo = MongoCli(MONGO_DB)
db = mongo.Checker
users_db = db.users
stripe_db = db.stripe
premiumdb = db.premiums


async def get_users():
    user_list = []
    async for user in users_db.find({"id": {"$gt": 0}}):
        user_list.append(user['id'])
    return user_list

async def get_user(user):
  users = await get_users()
  if user in users:
    return True
  else:
    return False

async def add_user(user):
    if await get_user(user):
        return
    await users_db.insert_one({"id": int(user)})

async def del_user(user):
    if not await get_user(user):
        return
    await users_db.delete_one({"id": int(user)})


async def update_user(user_data):
    await premiumdb.update_one({"id": int(user_data["id"])}, {"$set": user_data}, upsert=True)

async def has_premium_access(user_id):
    user_data = await premiumdb.find_one({"id": int(user_id)})
    if user_data:
        expiry_time = user_data.get("expiry_time")
        if isinstance(expiry_time, datetime) and datetime.now() <= expiry_time:
            return True
        else:
            await premiumdb.update_one({"id": int(user_id)}, {"$set": {"expiry_time": None}})
    return False


async def check_remaining_uasge(user_id):
    user_data = await premiumdb.find_one({"id": int(user_id)})
    if user_data and user_data.get("expiry_time"):
        expiry_time = user_data["expiry_time"]
        remaining_time = expiry_time - datetime.now()
        return remaining_time
    return timedelta(0)


async def save_keys(sk, pk, merchant):
    await stripe_db.update_one({"owner_id": OWNER_ID}, {"$set": {"sk": sk, "pk": pk, "merchant": merchant}}, upsert=True)

async def delete_keys():
    await stripe_db.update_one({"owner_id": OWNER_ID}, {"$unset": {"sk": "", "pk": "", "merchant": ""}})

async def check_keys():
    result = await stripe_db.find_one({"owner_id": OWNER_ID}, {"sk": 1, "pk": 1, "merchant": 1})
    
    if result:
        return result.get('sk', False), result.get('pk', False), result.get('merchant', False)
    
    return (False, False, False)



class PremiumUser:
    def __init__(self, user_id, expiry_time):
        self.id = user_id
        self.expiry_time = expiry_time


async def all_premium_users():
    cursor = premiumdb.find({
        "expiry_time": {"$gt": datetime.now()}
    })

    async def process_user(user):
        user_id = user.get("id")
        try:
            user_data = await app.get_users(user_id)
            if user_data:
                user_data.expiry_time = user.get("expiry_time")  # Add expiry_time to the user data
                return user_data
        except Exception:
            return PremiumUser(user_id, user.get("expiry_time"))
    
    premium_users = await asyncio.gather(
        *[process_user(user) async for user in cursor]
    )
    
    return [user for user in premium_users if user is not None]
