import os
import re
import json
import random
import string
import logging
import requests
import urllib.request
from shutil import rmtree
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pyrogram.errors.exceptions
from pyrogram import Client, filters

load_dotenv()
COMMANDS_STR = str(os.getenv("COMMANDS"))
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


async def crfile(client, chat, text, title="links", out="./Downloads/"):
    file = f"{out}{title}.txt"
    if not os.path.isdir(out):
        os.makedirs(out)
    with open(file, "w") as w:
        w.write(text)
    await client.send_document(chat_id=chat,
                               document=file)
    rmtree(out)


async def ta_s(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    script = soup.find_all("script")[-2]
    lest = script.contents[0].strip().split(";")[0].split("var videos = ")[1]
    json_dumps = lest.replace(
        "[", "{").replace("]", "}").replace("},{", ",").replace(
        "\\", "").replace('","', '":"').replace(",0", "")[1:-1]
    json_bruh = json.loads(json_dumps).values()
    soup = BeautifulSoup(r.content, 'html.parser')
    lnk = []
    for i in json_bruh:
        lnk.append(i)
    for script in soup.find_all(attrs={"class": "btn btn-success btn-download btn-sm rounded-pill"}):
        url = script['href']
        lnk.append(url)
    return lnk


async def scrap(client, message):
    title = ""
    chat = message["chat"]["id"]
    command = message["command"][0]
    text = " ".join(message["text"].split(" ")[1:])
    # Temp Directory
    key = string.hexdigits
    session_random = "".join([random.choice(key) for i in range(5)])
    tmp_directory = f"./Downloads/{message['from_user']['id']}/{session_random}/"
    config = text.split("|")
    url = config[0]
    # if "http" not in url:
    #     url = "https://" + url
    regex = False
    if "|" in text:
        regex = config[1]
    try:
        r = requests.get(url).content
    except requests.exceptions.MissingSchema as e:
        index = re.search(r"http[\w]{0,1000}", e.args[0]).start()
        url = e.args[0][index:-1]
        r = requests.get(url).content
    try:
        host = urllib.request.Request(url).host
    except Exception as e:
        print(e)
        host = None
    soup = BeautifulSoup(r, "html.parser")
    if "f" in command:
        ht = re.findall(r'"https?://[\s]{0,1000}[\S]{0,1000}"', str(r))
        alll = [i.replace('"', "") for i in ht]
        try:
            if "tioanime" in host:
                u = await ta_s(url)
                for i in u:
                    alll.append(i)
        except IndexError:
            logging.info("IndexError, no hay links de capítulos")
    if "t" in command:
        alll = []
        if "tioanime" in host:
            title = soup.find("h1").text
            u = await ta_s(url)
            for i in u:
                alll.append(i)
    else:
        a = soup.find_all("a")
        alll = [b.get("href") for b in a]
    c = []
    for i in alll:
        if i[0] == "/" and host is not None:
            c.append(host + i)
        else:
            c.append(i)
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
    out = tmp_directory
    try:
        if "t" in command:
            await crfile(client, chat, text, title, out)
        else:
            await message.edit(text)
    except pyrogram.errors.MessageEmpty:
        await message.edit("No se encontro nada o hubo un error en la busqueda")
    except pyrogram.errors.MessageTooLong:
        await crfile(client, chat, text, out=out)


@Client.on_message(filters.user(ADMINS) & filters.command(["scrap", "sc", "scrapf", "scf", "sct"], COMMANDS))
async def scrap_web(client, message):
    await scrap(client, message)
