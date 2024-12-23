# https://t.me/Ultroid_Official/524

from pyrogram import __version__, Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from database.database import full_userbase
from bot import Bot
from config import OWNER_ID, ADMINS, CHANNEL, SUPPORT_GROUP, OWNER
from plugins.cmd import *

# Callback query handler
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text=f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n"
                 f"○ Language : <code>Python3</code>\n"
                 f"○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n"
                 f"○ Source Code : <a href='https://youtu.be/BeNBEYc-q7Y'>Click here</a>\n"
                 f"○ Channel : @{CHANNEL}\n"
                 f"○ Support Group : @{SUPPORT_GROUP}</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔒 Close", callback_data="close")]]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except Exception as e:
            print(f"Error deleting reply-to message: {e}")

    elif data == "upi_info":
        await upi_info(client, query.message)

    elif data == "show_plans":
        await show_plans(client, query.message)

    elif data == "refer":
        # Since `referral_command` expects `message`, pass the correct `user_id`
        user_id = query.from_user.id  # Get the user ID from the callback query
        bot_username = (await client.get_me()).username
        rlink = f"https://t.me/{bot_username}?start=refer_{user_id}"

        await query.message.reply(
            f"Your referral link:\n{rlink}\n"
            "Share this link with others to earn benefits!"
        )

    elif data == "time":
        # Since `status_command` expects `message`, you need to simulate this from the callback query
        user_id = query.from_user.id  # Get the user ID from the callback query
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

        await query.message.reply(status_message)

        
# https://t.me/Ultroid_Official/524


# ultroidofficial : YT



