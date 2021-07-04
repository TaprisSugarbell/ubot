import os
import speedtest
from dotenv import load_dotenv
from pyrogram import Client, filters

load_dotenv()
COMMANDS_STR = os.getenv("COMMANDS")
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


@Client.on_message(filters.user(ADMINS) & filters.command(["speed"], COMMANDS))
async def speed(client, message):
    s = speedtest.Speedtest()
    s.download()
    s.upload()
    results = s.results.dict()
    ping = results["ping"]
    download = results["download"]/1000000
    upload = results["upload"]/1000000
    await message.edit(f"**Ping:** {ping:.2f} ms\n"
                       f"**Download:** {download:.2f} MB/s\n"
                       f"**Upload:** {upload:.2f} MB/s")


