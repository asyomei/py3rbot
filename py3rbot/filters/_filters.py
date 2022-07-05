from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message


# @filters.create
# async def reply_to_me(_, app: Client, message: Message) -> bool:
#     if not message.reply_to_message:
#         return False
#     me = await app.get_me()
#     return message.reply_to_message.from_user.id == me.id


@filters.create
async def via_me(_, app: Client, message: Message) -> bool:
    if not message.via_bot:
        return False
    me = await app.get_me()
    return message.via_bot.id == me.id
