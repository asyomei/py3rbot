from platform import python_version

from pyrogram.client import Client
from pyrogram.filters import command
from pyrogram.types import Message

from .. import strings


@Client.on_message(command("start")) # pyright: ignore
async def start_cmd(_, message: Message) -> None:
    text = strings.start_message()
    await message.reply(text, quote=False)

@Client.on_message(command("help")) # pyright: ignore
async def help_cmd(_, message: Message) -> None:
    text = strings.help_message(python_version())
    await message.reply(text, quote=False)

@Client.on_message(command("py")) # pyright: ignore
async def py_cmd_noargs(_, message: Message) -> None:
    if len(message.command) > 1:
        message.continue_propagation()
    text = strings.py_message()
    await message.reply(text, quote=False)

@Client.on_message(command("inline")) # pyright: ignore
async def inline_cmd(app: Client, message: Message) -> None:
    me = await app.get_me()
    text = strings.inline_message(me.username)
    await message.reply(text, quote=False)
