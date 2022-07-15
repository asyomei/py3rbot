from pyrogram.client import Client
from pyrogram.filters import create as create_filter
from pyrogram.types import Message


@create_filter
async def via_me(_, app: Client, message: Message) -> bool:
    if not message.via_bot:
        return False
    me = await app.get_me()
    return message.via_bot.id == me.id
