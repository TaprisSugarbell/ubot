import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TOKEN = os.getenv("BOT_TOKEN")

ubot = Client("ubot", api_id=API_ID, api_hash=API_HASH)


if __name__ == "__main__":
    ubot.run()
