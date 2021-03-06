import os
import zipfile
from shutil import rmtree
from dotenv import load_dotenv
from pyrogram import Client, filters
from helper.files_ import file_recognize
from rarfile import RarFile, PasswordRequired

load_dotenv()
COMMANDS_STR = str(os.getenv("COMMANDS"))
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


@Client.on_message(filters.user(ADMINS) & filters.command(["unrar"], COMMANDS))
async def unrar_file(client, message):
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
            files = [zip_ + i for i in os.listdir(zip_)]
            for fil in files:
                recog = await file_recognize(fil)
                if recog == "image":
                    await client.send_photo(chat_id=chat,
                                            photo=fil)
                    await client.send_document(chat_id=chat,
                                               document=fil)
                elif recog == "video":
                    await client.send_video(chat_id=chat,
                                            video=fil)
                elif recog == "document":
                    await client.send_document(chat_id=chat,
                                               document=fil)
                else:
                    pass
            rmtree(tmp_direct)
        except PasswordRequired:
            rmtree(tmp_direct)
            await message.edit("El archivo requiere contrase??a")
        except Exception as e:
            rmtree(tmp_direct)
            await message.edit(e)

