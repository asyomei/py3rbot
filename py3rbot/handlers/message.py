from platform import python_version

from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.filters import Filter, command, create as create_filter, private
from pyrogram.handlers.handler import Handler
from pyrogram.types.messages_and_media import Message

from .. import strings
from ..constants import TIMEOUT
from ..python_runner import PythonRunner, from_eval
from .handler_decorator import on_message
from .utils import code_args_split, get_formatted, html_italic


handlers = list[tuple[Handler, int]]()
on_message = on_message(handlers)


@create_filter
async def reply_to_me(_: Filter, app: Client, message: Message) -> bool:
    if not message.reply_to_message:
        return False
    me = await app.get_me()
    return message.reply_to_message.from_user.id == me.id


@create_filter
async def via_me(_: Filter, app: Client, message: Message) -> bool:
    if not message.via_bot:
        return False
    me = await app.get_me()
    return message.via_bot.id == me.id


@on_message(command("start"))
async def start_cmd(_: Client, message: Message) -> None:
    text = strings.start()
    await message.reply(text, quote=False)


@on_message(command("help"))
async def help_cmd(_: Client, message: Message) -> None:
    text = strings.help(python_version())
    await message.reply(text, quote=False)


@on_message(command("inline"))
async def inline_cmd(app: Client, message: Message) -> None:
    bot = await app.get_me()
    text = strings.inline_help(bot.username)
    await message.reply(text, quote=False)


@on_message(command("eval"))
async def eval_cmd(_: Client, message: Message) -> None:
    text = strings.eval_help()
    await message.reply(text, quote=False)


@on_message(command("py"))
async def py_cmd(app: Client, message: Message) -> None:
    _, *args = message.text.split(maxsplit=1)

    if not args:
        text = strings.py_cmd_help()
        await message.reply(text, quote=False)
        return

    await _send_result(app, message.chat.id, args[0])


@on_message((private | reply_to_me) & ~via_me)
async def on_reply(app: Client, message: Message) -> None:
    await _send_result(app, message.chat.id, message.text)


async def _send_result(app: Client, chat_id: int, text: str) -> None:
    code, args = code_args_split(text)

    text = html_italic(strings.running())
    m = await app.send_message(chat_id, text, ParseMode.HTML)

    if "e" in args:
        code = from_eval(code)

    result = await PythonRunner.run(code, TIMEOUT)
    result = get_formatted(result)
    await m.edit(result, ParseMode.HTML)
