# Import required libraries and modules
from bot import Bot
from pyrogram import Client, filters
from config import *
from datetime import datetime
from plugins.start import *
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
import time
from database.database import *

@Bot.on_message(filters.command('time') & filters.private )
async def status_command(bot: Bot, message: Message):
    user_id = message.from_user.id
    verify_status = await db_verify_status(user_id)

    is_verified = verify_status.get("is_verified", False)
    verified_time = verify_status.get("verified_time", 0)
    referred_by = verify_status.get("referrer", None)

    status_message = (
        f"Your Status:\n"
        f"- Verified: {'Yes' if is_verified else 'No'}\n"
        f"- Verification Time: {time.ctime(verified_time) if verified_time else 'N/A'}\n"
        f"- Referred By: {referred_by if referred_by else 'None'}"
    )
    await message.reply(status_message)

@Client.on_message(filters.command('refer') & filters.private )
async def referral_command(client: Client, message: Message):
    user_id = message.from_user.id  # Correctly get the user ID
    bot_username = (await client.get_me()).username  # Get the bot's username dynamically
    rlink = f"https://t.me/{bot_username}?start=refer_{user_id}"  # Use the correct user ID here

    await message.reply(
        f"Your referral link:\n{rlink}\n"
        "Share this link with others to earn benefits!"
    )


# /help command to show available commands
@Bot.on_message(filters.command('help') & filters.private )
async def help_command(bot: Bot, message: Message):
    help_text = """
📖 <b>Available Commands:</b>

/start - Start the bot and see welcome message.
/help - Show this help message.
/time - check your token time
/refer - get your refer link
/myplan - Check your premium status
/batch - Create link for more than one posts.
/genlink - Create link for one post.
/stats - Check your bot uptime.
/users - View bot statistics (Admins only).
/broadcast - Broadcast any messages to bot users (Admins only).
/addpr id days - Add credits to your account (Admins only).
/removepr id - remove premium user
/getpremiumusers - all premium user d and remaining time
/plans - Show available premium plans.
/upi - Show UPI payment options.
"""
    await message.reply(help_text, parse_mode=ParseMode.HTML)


# Command to add a premium subscription for a user (admin only)
@Bot.on_message(filters.private & filters.command('addpr') & filters.user(ADMINS))
async def add_premium(bot: Bot, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("You don't have permission to add premium users.")

    try:
        args = message.text.split()
        if len(args) < 3:
            return await message.reply("Usage: /addpr 'user_id' 'duration_in_days'")
        
        target_user_id = int(args[1])
        duration_in_days = int(args[2])
        await add_premium_user(target_user_id, duration_in_days)
        await message.reply(f"User {target_user_id} added to premium for {duration_in_days} days.")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

# Command to remove a premium subscription for a user (admin only)
@Bot.on_message(filters.private & filters.command('removepr') & filters.user(ADMINS))
async def remove_premium(bot: Bot, message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("You don't have permission to remove premium users.")

    try:
        args = message.text.split()
        if len(args) < 2:
            return await message.reply("Usage: /removepr 'user_id'")
        
        target_user_id = int(args[1])
        await remove_premium_user(target_user_id)
        await message.reply(f"User {target_user_id} removed from premium.")
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@Bot.on_message(filters.command('myplan') & filters.private)
async def my_plan(bot: Bot, message: Message):
    is_premium, expiry_time = await get_user_subscription(message.from_user.id)
    
    if is_premium and expiry_time:
        time_left = int(expiry_time - time.time())
        
        if time_left > 0:
            days_left = time_left // 86400
            hours_left = (time_left % 86400) // 3600
            minutes_left = (time_left % 3600) // 60

            response_text = (
                f"✅ Your premium subscription is active.\n\n"
                f"🕒 Time remaining: {days_left} days, {hours_left} hours, {minutes_left} minutes."
            )
            
            buttons = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Upgrade Plan", callback_data="show_plans")],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")],
                    [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
                ]
            )
        else:
            # Subscription expired
            response_text = (
                "⚠️ Your premium subscription has expired.\n\n"
                "Renew your subscription to continue enjoying premium features."
                "\nCheck: /plans"
            )
            
            buttons = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Renew Plan", callback_data="show_plans")],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")],
                    [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
                ]
            )

    else:
        # User is not a premium member
        response_text = "❌ You are not a premium user.\nView available plans to upgrade.\n\nClick HERE: /plans"
        
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("View Plans", callback_data="show_plans")],
                [InlineKeyboardButton("🔒 Close", callback_data="close")],
                [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
            ]
        )

    await message.reply_text(response_text, reply_markup=buttons)


# Command to show subscription plans
@Bot.on_message(filters.command('plans') & filters.private)
async def show_plans(bot: Bot, message: Message):
    plans_text = PAYMENT_TEXT 
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Pay via UPI", callback_data="upi_info")],
        [InlineKeyboardButton("🔒 Close", callback_data="close")],
        [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
    ])
    await message.reply(plans_text, reply_markup=buttons, parse_mode=ParseMode.HTML)

# Command to show UPI payment QR code and instructions
@Bot.on_message(filters.command('upi') & filters.private)
async def upi_info(bot: Bot, message: Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=PAYMENT_QR,
        caption=PAYMENT_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Contact Owner", url=f"https://t.me/{OWNER}")],
                [InlineKeyboardButton("🔒 Close", callback_data="close")]
            ]
        )
    )

# Command to retrieve a list of active premium users (admin only)
@Bot.on_message(filters.private & filters.command('getpremiumusers') & filters.user(ADMINS))
async def get_premium_users(bot: Bot, message: Message):
    try:
        premium_users = phdlust.find({"is_premium": True, "expiry_time": {"$gt": time.time()}})
        if not phdlust.count_documents({"is_premium": True, "expiry_time": {"$gt": time.time()}}):
            return await message.reply("No active premium users found.")

        users_list = [
            f"User ID: {user.get('user_id')} - Premium Expires in {max(int((user.get('expiry_time') - time.time()) / 86400), 0)} days"
            for user in premium_users
        ]
        await message.reply("<b>Premium Users:</b>\n\n" + "\n".join(users_list), parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")
