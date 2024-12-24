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
            text=f"ㅤㅤㅤ⌠ 𝗕𝗹𝗼𝗼𝗱𝘀 𝗡𝗲𝘁𝘄𝗼𝗿𝗸 🍀⌡\n\n"
                 f"◉ Bʟᴏᴏᴅs Sɪᴛᴇʀɪᴘ - @{CHANNEL}\n"
                 f"◉ Bʟᴏᴏᴅs Oɴʟʏғᴀɴs - @{SUPPORT_GROUP}</b>"
                 f"◉ Cʀᴇᴀᴛᴇʀ - <a href='tg://user?id={OWNER_ID}'>Saint</a>",
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

    elif data == "premium":
        await query.message.edit_text(
            text="Choose an option:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Buy Silver", callback_data="buy_silver")],
                    [InlineKeyboardButton("Buy Gold", callback_data="buy_gold")],
                    [InlineKeyboardButton("Buy Diamond", callback_data="buy_diamond")],
                    [InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
        )
    elif data == "buy_silver":
        await query.message.edit_text(
            text=(
                "<b><u>Silver Plan</u></b>\n\n"
                "1 Month - 50 INR\n"
                "<pre>≡ This plan provides premium access for our current bot with no Ads.</pre>\n"
                "⩉ <a href='https://i.ibb.co/nrmbSkG/file-3262.jpg'>Click To Get QR</a>\n"
                "⌕ For other payment methods, contact @odacchi.\n\n"
                "<b>Note: This plan is separate and lets you use bots without verification (Ads) only. Limits will remain the same as before.</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Back", callback_data="premium")],
                    [InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
        )
    elif data == "buy_gold":
        await query.message.edit_text(
            text=(
                "<b><u>Gold Plan</u></b>\n\n"
                "1 Month - 100 INR\n"
                "<pre>≡ This plan provides premium access for our two bots with no Ads.</pre>\n"
                "⩉ <a href='https://i.ibb.co/nrmbSkG/file-3262.jpg'>Click To Get QR</a>\n"
                "⌕ For other payment methods, contact @odacchi.\n\n"
                "<b>Note: This plan is separate and lets you use bots without verification (Ads) only. Limits will remain the same as before.</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Back", callback_data="premium")],
                    [InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
        )
    elif data == "buy_diamond":
        await query.message.edit_text(
            text=(
                "<b>Diamond Plan</b>\n\n"
                "1 Month - 150 INR\n"
                "<pre>≡ This plan provides premium access for our bots with no Ads.</pre>\n"
                "⩉<a href='https://i.ibb.co/nrmbSkG/file-3262.jpg'>Click To Get QR</a>\n"
                "⌕ For other payment methods, contact @odacchi.\n\n"
                "<b>Note: This plan is separate and lets you use bots without verification (Ads) only. Limits will remain the same as before.</b>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Back", callback_data="premium")],
                    [InlineKeyboardButton("Close", callback_data="close")]
                ]
            )
        )

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



