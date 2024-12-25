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

# Command: Add a Channel
@Bot.on_message(filters.command("add_channel") & filters.user(ADMINS))  # ADMINS = Admin User ID
async def add_force_sub_channel(client, message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            await message.reply("Usage: /add_channel <channel_id>")
            return
        channel_id = int(args[1])
        await add_channel(channel_id)
        await message.reply(f"✅ Channel {channel_id} has been added to the force-subscription list.")
    except Exception as e:
        await message.reply(f"❌ Error adding channel: {e}")

# Command: Remove a Channel
@Bot.on_message(filters.command("remove_channel") & filters.user(ADMINS))
async def remove_force_sub_channel(client, message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) != 2:
            await message.reply("Usage: /remove_channel <channel_id>")
            return
        channel_id = int(args[1])
        await remove_channel(channel_id)
        await message.reply(f"✅ Channel {channel_id} has been removed from the force-subscription list.")
    except Exception as e:
        await message.reply(f"❌ Error removing channel: {e}")

# Command: List All Channels
@Bot.on_message(filters.command("list_channels") & filters.user(ADMINS))
async def list_force_sub_channels(client, message):
    try:
        channels = await list_channels()
        if not channels:
            await message.reply("No channels in the force-subscription list.")
            return
        channel_list = "\n".join([f"- {channel_id}" for channel_id in channels])
        await message.reply(f"📜 Force-Subscription Channels:\n{channel_list}")
    except Exception as e:
        await message.reply(f"❌ Error listing channels: {e}")


@Bot.on_message(filters.command('profile') & filters.private)
async def time_command(client: Client, message: Message):
    user_id = message.from_user.id
    verify_status = await db_verify_status(user_id)

    is_verified = verify_status.get("is_verified", False)
    verified_time = verify_status.get("verified_time", 0)
    referral_count = verify_status.get("referral_count", 0)
    referrer = verify_status.get("referrer", None)

    remaining_time = (
        max(0, int(verified_time - time.time())) if is_verified else "N/A"
    )
    referral_status = (
        f"Yes (Referred by {referrer})" if referrer else "No Referrer"
    )

    status_message = (
        f"🔍 Your Verification Status 🔍\n\n"
        f"- Verified: {'✅ Yes' if is_verified else '❌ No'}\n"
        f"- Referral Status: {referral_status}\n"
        f"- Remaining Usage Time: {remaining_time if remaining_time == 'N/A' else f'{remaining_time // 3600} hrs {remaining_time % 3600 // 60} mins'}\n"
        f"- Referrals Made: {referral_count}\n\n"
        f"📌 Keep referring friends to earn more usage time!"
    )
    await message.reply(status_message)


@Bot.on_message(filters.command('refer') & filters.private)
async def refer_command(client: Client, message: Message):
    user_id = message.from_user.id
    referral_link = f"https://t.me/{client.username}?start=refer_{user_id}"
    verify_status = await db_verify_status(user_id)

    referral_count = verify_status.get("referral_count", 0)

    referral_message = (
        f"🚀 Your Personal Referral Link 🚀\n\n"
        f"📎 Link: {referral_link}\n\n"
        f"🎉 How it Works:\n"
        f"- Share this link with your friends.\n"
        f"- When they join, both of you get an extra {REFERTIME} hours of usage time!\n"
        f"- The more friends you refer, the more time you earn!\n\n"
        f"📊 Your Referral Stats:\n"
        f"- Referrals Made: {referral_count}\n\n"
        f"Keep sharing and enjoy the benefits!"
    )
    await message.reply(referral_message)



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
                    [InlineKeyboardButton("Upgrade Plan", callback_data="premium")],
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
                    [InlineKeyboardButton("Renew Plan", callback_data="premium")],
                    [InlineKeyboardButton("🔒 Close", callback_data="close")],
                    [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
                ]
            )

    else:
        # User is not a premium member
        response_text = "❌ You are not a premium user.\nView available plans to upgrade.\n\nClick HERE: /plans"
        
        buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("View Plans", callback_data="premium")],
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
        [InlineKeyboardButton("Pay via UPI", callback_data="premium")],
        [InlineKeyboardButton("🔒 Close", callback_data="close")],
        [InlineKeyboardButton("Contact Support", url=f"https://t.me/{OWNER}")]
    ])
    await message.reply(plans_text, reply_markup=buttons, parse_mode=ParseMode.HTML)

# Command to show UPI payment QR code and instructions
@Bot.on_message(filters.command('upi') & filters.private)
async def upi_info(bot: Bot, message: Message):
    plans_text = PAYMENT_TEXT
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝖡𝗎𝗒 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 | 𝖭𝗈 𝖠𝖽𝗌", callback_data="premium")],
        [InlineKeyboardButton("Contact Owner", url=f"https://t.me/{OWNER}")],
        [InlineKeyboardButton("🔒 Close", callback_data="close")]
    ])
    await message.reply(plans_text, reply_markup=buttons, parse_mode=ParseMode.HTML)

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
