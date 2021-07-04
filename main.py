import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = str(os.getenv("API_HASH"))
SAYUSESSION = str(os.getenv("SAYUSESSION"))
TOKEN = str(os.getenv("BOT_TOKEN"))

ubot = Client(SAYUSESSION, api_id=API_ID, api_hash=API_HASH)


if __name__ == "__main__":
    ubot.run()
