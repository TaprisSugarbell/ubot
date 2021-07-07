import os
import heroku3
from dotenv import load_dotenv
from pyrogram import Client, filters

# ADMINS and COMMANDS
load_dotenv()
APP_NAME = os.getenv("APP_NAME")
ADMINS_STR = os.getenv("ADMINS")
HEROKU_API = os.getenv("HEROKU_API")
CLIENT = heroku3.from_key(HEROKU_API)
COMMANDS_STR = str(os.getenv("COMMANDS"))
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


@Client.on_message(filters.user(ADMINS) & filters.command(["restart", "rt"], COMMANDS))
async def command(client, message):
    await message.edit(f"Reiniciando {APP_NAME}...")
    app = CLIENT.app(APP_NAME)
    app.restart()
