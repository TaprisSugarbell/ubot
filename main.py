import os
import asyncio
import logging
from pyrogram import Client
from dotenv import load_dotenv
from plugins.sayu_logs import date

logging.basicConfig(filename="sayu.log", level=logging.DEBUG, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARNING)

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = str(os.getenv("API_HASH"))
SAYUSESSION = str(os.getenv("SAYUSESSION"))
TOKEN = str(os.getenv("BOT_TOKEN"))
LOOP = asyncio.get_event_loop()

ubot = Client(SAYUSESSION, api_id=API_ID, api_hash=API_HASH)


# async def start_ubot():
#     try:
#         await ubot.start()
#         await idle()
#     finally:
#         await ubot.stop()


if __name__ == "__main__":
    # LOOP.run_until_complete(start_ubot())
    try:
        ubot.run()
    except Exception as e:
        asyncio.get_event_loop().run_until_complete(date(ubot, "ERROR\n", e))
