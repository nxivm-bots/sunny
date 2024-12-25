# https://t.me/ultroid_official

import os
import logging
from logging.handlers import RotatingFileHandler

DEFAULT_CHANNELS = [
    int(os.environ.get("FORCE_SUB_CHANNEL", "-1001677928096")),
    int(os.environ.get("FORCE_SUB_CHANNEL2", "-1001707354372")),
    int(os.environ.get("FORCE_SUB_CHANNEL3", "-1002340976260")),
    int(os.environ.get("FORCE_SUB_CHANNEL4", "-1001707354372")),
]


TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8188039296:AAGZYYRAZf28KY8Nc-Vw0LblDkd4N28_zEc")
APP_ID = int(os.environ.get("APP_ID", "22505271"))
API_HASH = os.environ.get("API_HASH", "c89a94fcfda4bc06524d0903977fc81e")
 
BAN = int(os.environ.get("BAN", "11100131910")) #Owner user id - dont chnge 
OWNER = os.environ.get("OWNER", "odacchi") #Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "1110013191")) #Owner user id
OWNER_USERNAME = os.environ.get('OWNER_USERNAME', 'odacchi')
SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP", "Bloods_Stashy") # WITHOUR @
CHANNEL = os.environ.get("CHANNEL", "Bloods_Onlyfans") # WITHOUR @


#pic
FORCE_PIC = os.environ.get("FORCE_PIC", "https://i.ibb.co/fp6p46v/file-5938.jpg")
START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/68cNy4b/file-5939.jpg")
TOKEN_PIC = os.environ.get("TOKEN_PIC", "https://i.ibb.co/fp6p46v/file-5938.jpg")
bot_username = os.environ.get("bot_username", "sunnyshare_bot")
REFERTIME = int(os.environ.get("REFERTIME",5)) #hours


#auto delete
DELETE_AFTER = int(os.environ.get("DELETE_AFTER", 1800)) #seconds
NOTIFICATION_TIME = int(os.environ.get('NOTIFICATION_TIME', 1800)) #seconds
AUTO_DELETE = os.environ.get("AUTO_DELETE", True) #ON/OFF
GET_AGAIN = os.environ.get("GET_AGAIN", False) #ON/OFF
DELETE_INFORM = os.environ.get("INFORM" , "Your Video / File Is Successfully Deleted ✅")
NOTIFICATION = os.environ.get("NOTIFICATION" ,f"ㅤㅤㅤ❕⌠  𝘐𝘔𝘗𝘖𝘙𝘛𝘈𝘕𝘛 ⌡ ❕\n\n◉ 「  𝘛𝘩𝘪𝘴 𝘷𝘪𝘥𝘦𝘰 / 𝘧𝘪𝘭𝘦 𝘸𝘪𝘭𝘭 𝘣𝘦 𝘥𝘦𝘭𝘦𝘵𝘦𝘥 𝘪𝘯 30 𝘮𝘪𝘯𝘶𝘵𝘦𝘴 (𝘋𝘶𝘦 𝘵𝘰 𝘤𝘰𝘱𝘺𝘳𝘪𝘨𝘩𝘵 𝘪𝘴𝘴𝘶𝘦𝘴  」\n\n◉ 「 𝘗𝘭𝘦𝘢𝘴𝘦 𝘧𝘰𝘳𝘸𝘢𝘳𝘥 𝘵𝘩𝘪𝘴 𝘷𝘪𝘥𝘦𝘰 / 𝘧𝘪𝘭𝘦 𝘵𝘰 𝘴𝘰𝘮𝘦𝘸𝘩𝘦𝘳𝘦 𝘦𝘭𝘴𝘦 𝘢𝘯𝘥 𝘴𝘵𝘢𝘳𝘵 𝘥𝘰𝘸𝘯𝘭𝘰𝘢𝘥𝘪𝘯𝘨 𝘵𝘩𝘦𝘳𝘦 」")
GET_INFORM = os.environ.get("GET_INFORM" ,f"File was deleted after {DELETE_AFTER} seconds. Use the button below to GET FILE AGAIN.")

#Premium varibles
PAYMENT_QR = os.getenv('PAYMENT_QR', 'https://i.ibb.co/nrmbSkG/file-3262.jpg')
PAYMENT_TEXT = os.getenv('PAYMENT_TEXT', 'To get Plan and payment details press the button (𝖡𝗎𝗒 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 | 𝖭𝗈 𝖠𝖽𝗌) below ')


DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://kratosnigger:GuH0qHewCzuynCE4@telegram.mhwll.mongodb.net/")
DB_NAME = os.environ.get("DATABASE_NAME", "sunny")

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002320610978")) #database save channel id 


FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1001677928096"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1001707354372"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "-1002340976260"))
FORCE_SUB_CHANNEL4 = int(os.environ.get("FORCE_SUB_CHANNEL4", "-1001707354372"))


SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "adrinolinks.in") 
SHORTLINK_API = os.environ.get("SHORTLINK_API", "89eebc6996b78477dabf7aebb318fc0e8055e8dc")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 21600)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/tutorita/11")


# ignore this one
SECONDS = int(os.getenv("SECONDS", "200")) # auto delete in seconds

PORT = os.environ.get("PORT", "9060")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")

try:
    ADMINS=[6698364560]
    for x in (os.environ.get("ADMINS", "6698364560 6933669203").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")


FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {mention}\n\n<b>You Need To Join Our Channels To Use Me.\n\nKindly Join Our Channels.</b>")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None) # remove None and fo this ->: "here come your txt" also with this " " 

PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot !"

ADMINS.append(OWNER_ID)
ADMINS.append(1110013191)

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
