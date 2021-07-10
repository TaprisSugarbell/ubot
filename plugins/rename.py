import os
import random
import string
from shutil import rmtree
from helper.utils import *
from dotenv import load_dotenv
from plugins.sayu_logs import date
from pyrogram import Client, filters
from helper.files_ import file_recognize

# ADMINS and COMMANDS
load_dotenv()
COMMANDS_STR = str(os.getenv("COMMANDS"))
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


@Client.on_message(filters.user(ADMINS) & filters.command(["rename", "rn"], COMMANDS))
async def rename(client, message):
    text = " ".join(message["text"].split(" ")[1:])
    chat = message["chat"]["id"]
    print(message)
    key = string.hexdigits
    session_random = "".join([random.choice(key) for i in range(5)])
    tmp_directory = f"./Downloads/{message['from_user']['id']}/{session_random}/"
    reply_to = message["reply_to_message"]
    media =reply_to["media"]
    if media:
        media_ = ["video", "audio", "document", "photo"]
        files = [reply_to[i] for i in media_]
        file = [i for i in files if i is not None][0]
        file_id, file_name = file["file_id"], file["file_name"]
        rute_file = tmp_directory + file_name
        ext = rute_file.split(".")[-1]
        # Obtener caption
        caption = reply_to["caption"]
        if caption is None:
            caption = ""
        # Descargar thumb
        try:
            thumb = file["thumbs"][0]["file_id"]
            await client.download_media(thumb, tmp_directory + "thumb.jpg")
        except TypeError:
            thumb = None
        await client.download_media(file_id, rute_file)
        # Renombrar
        if text.endswith(ext):
            os.rename(rute_file, tmp_directory + text)
            rut = tmp_directory + text
        else:
            os.rename(rute_file, tmp_directory + text + "." + ext)
            rut = tmp_directory + text + "." + ext
        # Reconocer el archivo
        ftype = await file_recognize(rut, tmp_directory)
        try:
            if "thumb.jpg" not in os.listdir(tmp_directory):
                await generate_screen_shots(rut, tmp_directory, 300, 1)
            thumb = True
        except Exception as e:
            print(e)
            thumb = False
        try:
            if ftype == "video":
                await upload_video(client, chat, tmp_directory, rut, thumb, caption)
            elif ftype == "image":
                await upload_photo(client, chat, rut, caption)
            elif ftype == "song":
                await upload_audio(client, chat, tmp_directory, rut, thumb, caption)
            else:
                await upload_document(client, chat, tmp_directory, rut, thumb, caption)
            rmtree(tmp_directory)
        except Exception as e:
            rmtree(tmp_directory)
            level = "ERROR"
            await date(client, level, e)
