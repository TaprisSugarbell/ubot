import os
import random
import string
import logging
from dotenv import load_dotenv
from pydub import AudioSegment
from pyrogram import Client, filters
from helper.files_ import file_recognize
from moviepy.editor import VideoFileClip
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


async def convert(filename):
    if filename[-4:] == "webm":
        file_ = filename[:-5] + ".mp3"
    else:
        file_ = filename[:-4] + ".mp3"
    aud = AudioSegment.from_file(r"{}".format(filename))
    aud.export(f"{file_}", format="mp3")
    return file_


async def upload_video(client, chat, tmp_directory, file, thumb):
    clip = VideoFileClip(file)
    time_ = clip.duration
    size = clip.size
    height = size[1]
    width = size[0]
    if thumb:
        await client.send_video(chat_id=chat,
                                video=file,
                                thumb=f"{tmp_directory}thumb.jpg",
                                duration=time_,
                                height=height,
                                width=width)
    else:
        await client.send_video(chat_id=chat,
                                video=file,
                                duration=time_,
                                height=height,
                                width=width)


async def upload_document(client, chat, tmp_directory, file, thumb):
    if thumb:
        await client.send_document(chat_id=chat,
                                   document=file,
                                   thumb=f"{tmp_directory}thumb.jpg")
    else:
        await client.send_document(chat_id=chat,
                                   document=file)


async def upload_photo(client, chat, file):
    await client.send_photo(chat_id=chat,
                            photo=file)


async def upload_audio(client, chat, tmp_directory, file, thumb):
    if thumb:
        await client.send_audio(chat_id=chat,
                                audio=file,
                                thumb=f"{tmp_directory}thumb.jpg")
    else:
        await client.send_audio(chat_id=chat,
                                audio=file)


@Client.on_message(filters.user(ADMINS) & filters.command(["yt", "ytf", "yta", "ytb"], COMMANDS))
async def yt(client, message):
    print(message)
    key = string.hexdigits
    session_random = "".join([random.choice(key) for i in range(5)])
    chat = message["chat"]["id"]
    command = message["command"][0]
    text = " ".join(message["text"].split(" ")[1:])
    # tmp_directory = f"./Downloads/{message['from_user']['id']}/{session_random}/"
    tmp_directory = f"./Downloads/{message['from_user']['id']}/D76bE/"
    file = await download_file(text, tmp_directory)
    ftype = await file_recognize(file, tmp_directory)
    try:
        await generate_screen_shots(file, tmp_directory, 300, 1)
        thumb = True
    except Exception as e:
        print(e)
        thumb = False
    if ftype == "video":
        if command == "ytf":
            await upload_document(client, chat, tmp_directory, file, thumb)
        elif command == "ytb":
            await upload_video(client, chat, tmp_directory, file, thumb)
            await upload_document(client, chat, tmp_directory, file, thumb)
        elif command == "yta":
            song = await convert(file)
            await upload_audio(client, chat, tmp_directory, song, thumb)
        else:
            await upload_video(client, chat, tmp_directory, file, thumb)
    elif ftype == "image":
        if command == "ytf":
            await upload_document(client, chat, tmp_directory, file, thumb)
        elif command == "ytb":
            await upload_photo(client, chat, file)
            await upload_document(client, chat, tmp_directory, file, thumb)
        else:
            await upload_photo(client, chat, file)
    elif ftype == "song":
        await upload_audio(client, chat, tmp_directory, file, thumb)
    else:
        await upload_document(client, chat, tmp_directory, file, thumb)