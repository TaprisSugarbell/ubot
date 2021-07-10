import os
import random
import string
import logging
from shutil import rmtree
from helper.utils import *
from dotenv import load_dotenv
from plugins.sayu_logs import date
from pyrogram import Client, filters
from helper.files_ import file_recognize
from helper.download import download_file
from helper.utils import generate_screen_shots

logging.basicConfig(filename="sayu.log", level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

load_dotenv()
COMMANDS_STR = str(os.getenv("COMMANDS"))
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


@Client.on_message(filters.user(ADMINS) & filters.command(["yt", "ytf", "yta", "ytb"], COMMANDS))
async def yt(client, message):
    print(message)
    key = string.hexdigits
    session_random = "".join([random.choice(key) for i in range(5)])
    chat = message["chat"]["id"]
    command = message["command"][0]
    string_ = " ".join(message["text"].split(" ")[1:])
    strplit = string_.split("|")
    text = strplit[0]
    tmp_directory = f"./Downloads/{message['from_user']['id']}/{session_random}/"
    # tmp_directory = f"./Downloads/{message['from_user']['id']}/D76bE/"
    file = await download_file(text, tmp_directory)
    ftype = await file_recognize(file, tmp_directory)
    if len(strplit) > 1:
        fil_ename = strplit[1]
        ext = file.split(".")[-1]
        if fil_ename.endswith(ext):
            os.rename(file, tmp_directory + fil_ename)
            file = tmp_directory + fil_ename
        else:
            os.rename(file, tmp_directory + fil_ename + "." + ext)
            file = tmp_directory + fil_ename + "." + ext
        try:
            caption = strplit[2]
        except IndexError:
            caption = ""
    else:
        caption = ""
    try:
        if "thumb.jpg" not in os.listdir(tmp_directory):
            await generate_screen_shots(file, tmp_directory, 300, 1)
        thumb = True
    except Exception as e:
        print(e)
        thumb = False
    try:
        if ftype == "video":
            if command == "ytf":
                await upload_document(client, chat, tmp_directory, file, thumb, caption)
            elif command == "ytb":
                await upload_video(client, chat, tmp_directory, file, thumb, caption)
                await upload_document(client, chat, tmp_directory, file, thumb)
            elif command == "yta":
                song = await convert(file)
                await upload_audio(client, chat, tmp_directory, song, thumb, caption)
            else:
                await upload_video(client, chat, tmp_directory, file, thumb, caption)
        elif ftype == "image":
            if command == "ytf":
                await upload_document(client, chat, tmp_directory, file, thumb, caption)
            elif command == "ytb":
                await upload_photo(client, chat, file, caption)
                await upload_document(client, chat, tmp_directory, file, thumb)
            else:
                await upload_photo(client, chat, file, caption)
        elif ftype == "song":
            await upload_audio(client, chat, tmp_directory, file, thumb, caption)
        else:
            await upload_document(client, chat, tmp_directory, file, thumb, caption)
        rmtree(tmp_directory)
    except Exception as e:
        rmtree(tmp_directory)
        level = "ERROR"
        await date(client, level, e)
