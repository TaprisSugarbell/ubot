import os
from dotenv import load_dotenv
from pyrogram import Client, filters

# ADMINS and COMMANDS
load_dotenv()
COMMANDS_STR = str(os.getenv("COMMANDS"))
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


@Client.on_message(filters.user(ADMINS) & filters.command(["install"], COMMANDS))
async def install(client, message):
    document = message["reply_to_message"]
    if document:
        file = document["document"]["file_id"]
        file_name = str(document["document"]["file_name"])
        if file_name.endswith(".py"):
            await client.download_media(file, "./plugins/" + file_name)
            await message.edit(f"Se ha instalado el plugin {file_name[:-3]}")
        else:
            await message.edit("Solo se permiten archivos python")
    else:
        await message.edit("Tienes que responder a un documento")
