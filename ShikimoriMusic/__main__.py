import asyncio
import requests

from telegram.ext import CommandHandler

from pyrogram import Client
from pytgcalls import idle

from ShikimoriMusic import LOGGER, pbot, application, ubot
from ShikimoriMusic.mongo.queue import get_active_chats, remove_active_chat
from ShikimoriMusic.calls.calls import run
from ShikimoriMusic.plugins.errors import error_callback
from ShikimoriMusic.plugins.gban import gban, gbanlist, ungban
from ShikimoriMusic.vars import API_ID, API_HASH, BOT_TOKEN, BG_IMG, OWNER_ID

response = requests.get(BG_IMG)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)

def main():
    application.add_handler(CommandHandler("gban", gban, block=False))
    application.add_handler(CommandHandler("ungban", ungban, block=False))
    application.add_handler(CommandHandler("gbanlist", gbanlist, block=False))
    application.run_polling(timeout=15, drop_pending_updates=False)
    application.add_error_handler(error_callback)

async def load_start():
    served_chats = []
    try:
        chats = get_active_chats()
        for chat in chats:
            served_chats.botend(int(chat["chat_id"]))
    except Exception as e:
        LOGGER.info("Error came while clearing db")
    for served_chat in served_chats:
        try:
            remove_active_chat(served_chat)
        except Exception as e:
            LOGGER.info("Error came while clearing db")
            pass
    #await pbot.send_message(OWNER_ID, "**Music Bot Started Successfully !!**")
   # Copyrighted Area
    LOGGER.info("[INFO]: STARTED")
    await pbot.send_message(
        -1001717154437, "**Pyrogram Client Started Successfully !!**"
    )
    LOGGER.info("[INFO]: PYROGRAM STARTED")
    await ubot.send_message(
        -1001717154437, "**Assistant Started Successfully !!**"
    )
    main()
    

loop = asyncio.get_event_loop_policy().get_event_loop()
loop.run_until_complete(load_start())

Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "ShikimoriMusic.plugins"},
).start()

run()
idle()
loop.close()
