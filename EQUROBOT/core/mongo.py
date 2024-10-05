from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from datetime import datetime, timedelta
from EQUROBOT import app
from config import OWNER_ID

mongo = MongoCli(MONGO_DB)
db = mongo.Checker
stripe_db = db.stripe
premiumdb = db.premiums

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
