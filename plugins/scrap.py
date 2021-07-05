import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pyrogram.errors.exceptions
from pyrogram import Client, filters

load_dotenv()
COMMANDS_STR = str(os.getenv("COMMANDS"))
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


async def scrap(client, message):
    chat = message["chat"]["id"]
    text = " ".join(message["text"].split(" ")[1:])
    config = text.split("|")
    url = config[0]
    regex = False
    if "|" in text:
        regex = config[1]
    r = requests.get(url).content
    soup = BeautifulSoup(r, "html.parser")
    # ht = re.findall(r'"https?://[\s]{0,1000}[\S]{0,1000}"', str(r))
    # regexz = [i.replace('"', "") for i in ht]
    a = soup.find_all("a")
    c = [b.get("href") for b in a]
    regxx = r"{}".format(regex)
    if regex:
        c = [i for i in c if len(re.findall(regxx, i)) > 0]
    text = ""
    # for i in regexz:
    #     text += f"{i}\n"
    for i in c:
        # if i is not None:
        text += f"{i}\n"
    # print(text)
    try:
        await message.edit(text)
    except pyrogram.errors.MessageEmpty:
        await message.edit("No se encontro nada o hubo un error en la busqueda")
    except pyrogram.errors.MessageTooLong:
        with open("./Downloads/links.txt", "w") as w:
            w.write(text)
        await client.send_document(chat_id=chat,
                                   document="./Downloads/links.txt")
        os.unlink("./Downloads/links.txt")


@Client.on_message(filters.user(ADMINS) & filters.command(["scrap", "sc"], COMMANDS))
async def scrap_web(client, message):
    await scrap(client, message)


