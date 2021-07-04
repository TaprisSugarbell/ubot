import os
import zipfile
from shutil import rmtree
from dotenv import load_dotenv
from pyrogram import Client, filters
from rarfile import RarFile, PasswordRequired

load_dotenv()
COMMANDS_STR = os.getenv("COMMANDS")
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


@Client.on_message(filters.user(ADMINS) & filters.command(["unrar"], COMMANDS))
async def unrar_file(client, message):
    print(message)
    tmp_direct = f"./Downloads/{message['from_user']['id']}/"
    if not os.path.isdir(tmp_direct):
        os.makedirs(tmp_direct)
    chat = message["chat"]["id"]
    text = " ".join(message["text"].split(" ")[1:])
    document = message["reply_to_message"]
    if document:
        file = document["document"]["file_id"]
        file_name = document["document"]["file_name"]
        await client.download_media(file, tmp_direct + file_name)
        zip_ = tmp_direct + os.listdir(tmp_direct)[0]
        try:
            RarFile(zip_).extractall(path=tmp_direct, pwd=text)
            os.unlink(zip_)
            zip_ = tmp_direct + os.listdir(tmp_direct)[0] + "/"
            files = [zip_ + i for i in os.listdir(zip_) if i.endswith(".jpg") or i.endswith(".png")]
            for fil in files:
                await client.send_document(chat_id=chat,
                                           document=fil)
            rmtree(tmp_direct)
        except PasswordRequired:
            rmtree(tmp_direct)
            await message.edit("El archivo requiere contraseña")

