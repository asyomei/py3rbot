from platform import python_version

from pyrogram.client import Client
from pyrogram.filters import command
from pyrogram.types import Message

from .. import strings


@Client.on_message(command("start")) # type: ignore
async def start_cmd(_, message: Message) -> None:
    text = strings.start()
    await message.reply(text, quote=False)


@Client.on_message(command("help")) # type: ignore
async def help_cmd(_, message: Message) -> None:
    text = strings.help(python_version())
    await message.reply(text, quote=False)


@Client.on_message(command("py")) # type: ignore
async def py_cmd_noargs(_, message: Message) -> None:
    if len(message.text.split(maxsplit=1)) > 1:
        message.continue_propagation()

    text = strings.py_cmd_help()
    await message.reply(text, quote=False)


@Client.on_message(command("inline")) # type: ignore
async def inline_cmd(app: Client, message: Message) -> None:
    me = await app.get_me()
    text = strings.inline_help(me.username)
    await message.reply(text, quote=False)
