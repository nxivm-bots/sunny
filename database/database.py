
import motor.motor_asyncio
from config import DB_URI, DB_NAME ,REFERTIME


dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']

channels_collection = database['force_sub_channels']

# Utility to fetch all channels
async def get_all_channels():
    channel_docs = channels_collection.find()
    return [doc['channel_id'] async for doc in channel_docs]

# Add a new channel
async def add_channel(channel_id: int):
    await channels_collection.update_one(
        {'channel_id': channel_id},
        {'$set': {'channel_id': channel_id}},  # Upsert
        upsert=True
    )

# Remove a channel
async def remove_channel(channel_id: int):
    await channels_collection.delete_one({'channel_id': channel_id})

# List all channels
async def list_channels():
    return await get_all_channels()


default_verify = {
    'is_verified': False,
    'verified_time': 600,
    'verify_token': "",
    'link': "",
    'referrer': None,  # User ID of the referrer
    'referred': False,
    'referral_count': 0,  # Count of successful referrals

}


# Utility Functions
def new_user(user_id):
    return {
        '_id': user_id,
        'verify_status': default_verify.copy(),
    }

async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)
    return

async def db_verify_status(user_id):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id, verify):
    await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] async for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})
    return
