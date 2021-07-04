import os
from dotenv import load_dotenv
from pyrogram import Client, filters


load_dotenv()
COMMANDS_STR = os.getenv("COMMANDS")
COMMANDS = [i for i in COMMANDS_STR.split(" ")]
ADMINS_STR = os.getenv("ADMINS")
ADMINS = [int(i) for i in ADMINS_STR.split(" ")]


@Client.on_message(filters.user(ADMINS) & filters.command(["json"], COMMANDS))
async def pjson(client, message):
    message_ = message["reply_to_message"]
    if message_:
        await message.edit(f"`{message_}`")
    else:
        await message.edit("You have to reply to a message...")
    # chat = update.chat.id
    # message = update.message_id
    # tomessage = update.reply_to_message
    # if tomessage:
    #     await bot.edit_message_text(chat_id=chat,
    #                                 text=f"`{tomessage}`",
    #                                 message_id=message)
    # else:
    #     await bot.edit_message_text(chat_id=chat,
    #                                 text="You have to reply to a message...",
    #                                 message_id=message)
