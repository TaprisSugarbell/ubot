import os
import random
import string
import datetime
from dotenv import load_dotenv
from pyrogram import Client, filters

# ADMINS and COMMANDS
load_dotenv()
CHANNEL_ID = int(os.getenv("CHANNEL_LOG_ID"))
COMMANDS_STR = str(os.getenv("COMMANDS"))
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]
key = string.hexdigits
sss_random = "".join([random.choice(key) for i in range(5)])


async def date(client, level="", reason=""):
    dft = "%d/%m/%Y %H:%M:%S %p"
    now = datetime.datetime.now().strftime(dft)
    diff = datetime.timedelta(hours=6)
    date_ = datetime.datetime.strptime(now, dft) - diff
    await client.send_document(chat_id=CHANNEL_ID,
                               document="./sayu.log",
                               caption=f"#{sss_random}\n"
                                       f"#{level}\n{str(date_)}\n"
                                       f"{str(reason)}")


@Client.on_message(filters.user(ADMINS) & filters.command(["logs", "l"], COMMANDS))
async def sayulogs(client, message):
    level = "INFO"
    await date(client, level)


