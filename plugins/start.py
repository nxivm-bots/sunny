# line number 160-169 check for changes - token
from pymongo import MongoClient
import asyncio
import base64
import logging
import os
import random
import re
import string
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import *
from helper_func import subscribed, encode, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import *
from shortzy import Shortzy

#delete_after = 600

client = MongoClient(DB_URI)  # Replace with your MongoDB URI
db = client[DB_NAME]  # Database name
phdlust = db["phdlust"]  # Collection for users
phdlust_tasks = db["phdlust_tasks"] 

# MongoDB Helper Functions
async def add_premium_user(user_id, duration_in_days):
    expiry_time = time.time() + (duration_in_days * 86400)  # Calculate expiry time in seconds
    phdlust.update_one(
        {"user_id": user_id},
        {"$set": {"is_premium": True, "expiry_time": expiry_time}},
        upsert=True
    )

async def remove_premium_user(user_id):
    phdlust.update_one(
        {"user_id": user_id},
        {"$set": {"is_premium": False, "expiry_time": None}}
    )

async def get_user_subscription(user_id):
    user = phdlust.find_one({"user_id": user_id})
    if user:
        return user.get("is_premium", False), user.get("expiry_time", None)
    return False, None

async def is_premium_user(user_id):
    is_premium, expiry_time = await get_user_subscription(user_id)
    if is_premium and expiry_time > time.time():
        return True
    return False



# Function to add a delete task to the database
async def add_delete_task(chat_id, message_id, delete_at):
    phdlust_tasks.insert_one({
        "chat_id": chat_id,
        "message_id": message_id,
        "delete_at": delete_at
    })

# Function to delete the notification after a set delay
async def delete_notification(client, chat_id, notification_id, delay):
    await asyncio.sleep(delay)
    try:
        # Delete the notification message
        await client.delete_messages(chat_id=chat_id, message_ids=notification_id)
    except Exception as e:
        print(f"Error deleting notification {notification_id} in chat {chat_id}: {e}")
        
async def schedule_auto_delete(client, chat_id, message_id, delay):
    delete_at = datetime.now() + timedelta(seconds=int(delay))
    await add_delete_task(chat_id, message_id, delete_at)
    
    # Run deletion in the background to prevent blocking
    async def delete_message():
        await asyncio.sleep(int(delay))
        try:
            # Delete the original message
            await client.delete_messages(chat_id=chat_id, message_ids=message_id)
            phdlust_tasks.delete_one({"chat_id": chat_id, "message_id": message_id})  # Remove from DB
            
            # Send a notification about the deletion
            notification_text = DELETE_INFORM
            notification_msg = await client.send_message(chat_id, notification_text)
            
            # Schedule deletion of the notification after 60 seconds
            asyncio.create_task(delete_notification(client, chat_id, notification_msg.id, 40))
        
        except Exception as e:
            print(f"Error deleting message {message_id} in chat {chat_id}: {e}")

    asyncio.create_task(delete_message())  


async def delete_notification_after_delay(client, chat_id, message_id, delay):
    await asyncio.sleep(delay)
    try:
        # Delete the notification message
        await client.delete_messages(chat_id=chat_id, message_ids=message_id)
    except Exception as e:
        print(f"Error deleting notification {message_id} in chat {chat_id}: {e}")

import time

async def grant_referral_benefit(referrer_id, referred_id):
    # Logic for granting referral benefits to both the referrer and referred user
    # First, get the current status of the referrer and referred user from the database
    referrer_data = await db_verify_status(referrer_id)
    referred_data = await db_verify_status(referred_id)

    # If referrer data exists, update their verification status and time
    if referrer_data:
        referrer_data['is_verified'] = True
        referrer_data['verified_time'] = time.time() + (REFERTIME * 60 * 60)  # Add 4 hours
        await db_update_verify_status(referrer_id, referrer_data)  # Save updated referrer data

    # If referred user data exists, update their verification status and time
    if referred_data:
        referred_data['is_verified'] = True
        referred_data['verified_time'] = time.time() + (REFERTIME * 60 * 60)  # Add 4 hours
        await db_update_verify_status(referred_id, referred_data)  # Save updated referred user data

    print(f"Referral benefits granted to referrer {referrer_id} and referred user {referred_id}")


async def handle_referral(message, user_id, verify_status, client):
    # Check if the user is trying to use a referral link
    if "refer_" in message.text:
        _, rid = message.text.split("_", 1)  # Get the referrer ID

        # Check if the user is trying to refer themselves
        if rid == str(user_id):
            sent_message = await message.reply("You cannot refer yourself. Please try again.")
            return

        # Check if the user has already received a referral benefit
        if verify_status.get('referred', False):  # Default value is False if 'referred' key doesn't exist
            sent_message = await message.reply("You have already received your referral benefit.")
            return

        # Check if the referrer is valid
        # if verify_status.get('referrer') != rid:
        #     sent_message = await message.reply("Your referral is invalid. Try again by clicking /start.")
        #     return

        # Update the user's status to verified and add referral details
        await update_verify_status(user_id, is_verified=True, verified_time=time.time(), referrer=rid, referred=True)
        sent_message = await message.reply(f"Your token was successfully verified and is valid for {REFERTIME} hours.")

        # Check if the user has not been referred yet and update the referrer
        if verify_status.get('referrer') is None:
            # Update the user as referred and set the referrer
            await update_verify_status(user_id, referrer=rid, referred=True)

            # Grant benefits to the referrer (the one who shared the referral link)
            await grant_referral_benefit(rid , user_id)

            # Notify the user that their referral has been accepted
            return await message.reply("Referral accepted. Enjoy the benefits!")
     

@Bot.on_message(filters.command('start') & filters.private & subscribed )
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    UBAN = BAN  # Fetch the owner's ID from config
    user_id = id
    # Schedule the initial message for deletion after 10 minutes
    #await schedule_auto_delete(client, message.chat.id, message.id, delay=600)

    # Referral link for the user
    referral_link = f"https://t.me/{client.username}?start=refer_{user_id}"
           
    if id == UBAN:
        sent_message = await message.reply("You are the U-BAN! Additional actions can be added here.")
    else:
        if not await present_user(id):
            try:
                await add_user(id)
            except Exception as e:
                print(f"Error adding user: {e}")

        premium_status = await is_premium_user(id)
        verify_status = await get_verify_status(id)

        # Check verification status
        if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
            await update_verify_status(id, is_verified=False)
            
        await handle_referral(message, user_id, verify_status, client)

        # Handle token verification link
        if "verify_" in message.text:
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                sent_message = await message.reply("Your token is invalid or expired. Try again by clicking /start.")
                return
            await update_verify_status(id, is_verified=True, verified_time=time.time())
            sent_message = await message.reply("Your token was successfully verified and is valid for 6 hours.")

        
        elif len(message.text) > 7 and (verify_status['is_verified'] or premium_status):
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            ids = []

            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end+1) if start <= end else []
            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]

            temp_msg = await message.reply("Please wait...")

            try:
                messages = await get_messages(client, ids)
            except:
                error_msg = await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()

            phdlusts = []
            messages = await get_messages(client, ids)
            for msg in messages:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None
                
                try:
                    messages = await get_messages(client, ids)
                    phdlust = await msg.copy(chat_id=message.from_user.id, caption=caption, reply_markup=reply_markup , protect_content=PROTECT_CONTENT)
                    phdlusts.append(phdlust)
                    if AUTO_DELETE == True:
                        #await message.reply_text(f"The message will be automatically deleted in {delete_after} seconds.")
                        asyncio.create_task(schedule_auto_delete(client, phdlust.chat.id, phdlust.id, delay=DELETE_AFTER))
                    await asyncio.sleep(0.2)      
                    #asyncio.sleep(0.2)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    phdlust = await msg.copy(chat_id=message.from_user.id, caption=caption, reply_markup=reply_markup , protect_content=PROTECT_CONTENT)
                    phdlusts.append(phdlust)     

            # Notify user to get file again if messages are auto-deleted
            if GET_AGAIN == True:
                get_file_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("GET FILE AGAIN", url=f"https://t.me/{client.username}?start={message.text.split()[1]}")]
                ])
                await message.reply(GET_INFORM, reply_markup=get_file_markup)

            if AUTO_DELETE == True:
                delete_notification = await message.reply(NOTIFICATION)
                asyncio.create_task(delete_notification_after_delay(client, delete_notification.chat.id, delete_notification.id, delay=NOTIFICATION_TIME))
              
        elif verify_status['is_verified'] or premium_status:
            reply_markup = InlineKeyboardMarkup(
                [   
                    [InlineKeyboardButton("Refer Friends", callback_data="refer"), InlineKeyboardButton("Profile", callback_data="time")],
                    [InlineKeyboardButton("Premium", callback_data="premium"), InlineKeyboardButton("Close", callback_data="close")]
                    #[InlineKeyboardButton("✨ Premium", callback_data="upi_info")]
                ]
            )

            welcome_message = await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                #disable_web_page_preview=True,
                quote=True
            )
        else:
            verify_status = await get_verify_status(id)
            if IS_VERIFY and not verify_status['is_verified']:
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{client.username}?start=verify_{token}')
                buttons = [
                    [InlineKeyboardButton("Refer", callback_data="refer"), InlineKeyboardButton("￫ 𝖵𝖾𝗋𝗂𝖿𝗒", url=link)],
                    [InlineKeyboardButton("￫ 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅", url=TUT_VID)],
                    [InlineKeyboardButton("Premium", callback_data="premium")]
                ]
                verification_message = await message.reply_photo(
                    photo=TOKEN_PIC,  # This can be a URL or a file path
                    caption=f"Your token has EXPIRED !! \nRefresh Your Token to continue.\n\nToken Timeout: {get_exp_time(VERIFY_EXPIRE)}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    #protect_content=PROTECT_CONTENT,
                    quote=True
                )
                #await schedule_auto_delete(client, verification_message.chat.id, verification_message.id, delay=600)



    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink),
            InlineKeyboardButton(text="Join Channel", url=client.invitelink2),
        ],
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink3),
            #InlineKeyboardButton(text="Join Channel", url=client.invitelink4),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass


    # Prepare the message caption using formatted strings
    caption = FORCE_MSG.format(
        first=message.from_user.first_name,
        last=message.from_user.last_name,
        username=None if not message.from_user.username else '@' + message.from_user.username,
        mention=message.from_user.mention,
        id=message.from_user.id
    )

    # Send the photo with the inline keyboard buttons
    await message.reply_photo(
        photo=FORCE_PIC,  # This can be a URL or a file path
        caption=caption,
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,  # Quote the message to maintain context
        #disable_web_page_preview=True  # Disable web page preview if necessary
    )



@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
