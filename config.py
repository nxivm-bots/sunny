# https://t.me/ultroid_official

import os
import logging
from logging.handlers import RotatingFileHandler

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "706s")
APP_ID = int(os.environ.get("APP_ID", "225071"))
API_HASH = os.environ.get("API_HASH", "c89a4bc06524d0903977fc81e")
 
BAN = int(os.environ.get("BAN", "1198543450")) #Owner user id - dont chnge 
OWNER = os.environ.get("OWNER", "PhDLust") #Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "7131513396")) #Owner user id
OWNER_USERNAME = os.environ.get('OWNER_USERNAME', 'PhDLust')
SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP", "UOFFICIAL_CHAT") # WITHOUR @
CHANNEL = os.environ.get("CHANNEL", "ULTROID_OFFICIAL") # WITHOUR @


#pic
FORCE_PIC = os.environ.get("FORCE_PIC", "https://envs.sh/Ysc.jpg")
START_PIC = os.environ.get("START_PIC", "https://envs.sh/YLM.jpg")
TOKEN_PIC = os.environ.get("TOKEN_PIC", "https://envs.sh/Ysj.jpg")
bot_username = os.environ.get("bot_username", "deiimo_token_bot")
REFERTIME = int(os.environ.get("REFERTIME",4)) #hours


#auto delete
DELETE_AFTER = int(os.environ.get("DELETE_AFTER", 60)) #seconds
NOTIFICATION_TIME = int(os.environ.get('NOTIFICATION_TIME', 60)) #seconds
AUTO_DELETE = os.environ.get("AUTO_DELETE", True) #ON/OFF
GET_AGAIN = os.environ.get("GET_AGAIN", False) #ON/OFF
DELETE_INFORM = os.environ.get("INFORM" , "Successfully DELETED !!")
NOTIFICATION = os.environ.get("NOTIFICATION" ,f"File will delete after {DELETE_AFTER} seconds.")
GET_INFORM = os.environ.get("GET_INFORM" ,f"File was deleted after {DELETE_AFTER} seconds. Use the button below to GET FILE AGAIN.")

#Premium varibles
PAYMENT_QR = os.getenv('PAYMENT_QR', 'https://graph.org/file/c54fdc8a5580bb801abc2.jpg')
PAYMENT_TEXT = os.getenv('PAYMENT_TEXT', '<b>- ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs - \n\n'
                                      '- 20ʀs - 1 ᴡᴇᴇᴋ\n- 50ʀs - 1 ᴍᴏɴᴛʜ\n'
                                      '- 100ʀs - 3 ᴍᴏɴᴛʜs\n- 300ʀs - 6 ᴍᴏɴᴛʜs\n\n'
                                      '🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs 🎁\n\n'
                                      '○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ\n'
                                      '○ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n○ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n'
                                      '○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs & sᴇʀɪᴇs\n○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ\n'
                                      '✨ ᴜᴘɪ ɪᴅ - <code>dm : @jatin_24x for upi</code>\n\n'
                                      'ᴄʟɪᴄᴋ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ /myplan\n\n'
                                      '💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ\n\n'
                                      '‼️ ᴀғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ</b>')


DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluser10")

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-10020756565")) #database save channel id 
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-10021825006"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002135006"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "-1002182406"))
FORCE_SUB_CHANNEL4 = int(os.environ.get("FORCE_SUB_CHANNEL4", "-100218435006"))

#Shortner (token system) 
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "inshorturl.com") 
SHORTLINK_API = os.environ.get("SHORTLINK_API", "9f943360c339cec4fed66d9d5cbaa0c2b3d41f81")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 86400)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/Ultroid_Official/18")

# ignore this one
SECONDS = int(os.getenv("SECONDS", "200")) # auto delete in seconds

PORT = os.environ.get("PORT", "9090")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")

try:
    ADMINS=[6020516635]
    for x in (os.environ.get("ADMINS", "1198543451 6940013358 6020516635 1837294444 6695586027").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")


FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None) # remove None and fo this ->: "here come your txt" also with this " " 

PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot !"

ADMINS.append(OWNER_ID)
ADMINS.append(6695586027)

LOG_FILE_NAME = "uxblogs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   





# https://t.me/ultroid_official
