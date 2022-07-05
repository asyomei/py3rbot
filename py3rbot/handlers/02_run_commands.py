from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.filters import command, private
from pyrogram.types import Message
from pyrogram.types.messages_and_media.message import Str

from .. import strings
from ..constants import TIMEOUT
from ..filters import via_me
from ..utils import code_args_split, html_italic, py_run


@Client.on_message(command("py") & ~via_me) # type: ignore
async def py_command_args(app: Client, message: Message) -> None:
    text = message.text.split(maxsplit=1)[1]
    message.text = Str(text)
    await on_private(app, message)


@Client.on_message(private & ~via_me) # type: ignore
async def on_private(app: Client, message: Message) -> None:
    code, args = code_args_split(message.text)

    if not code:
        text = html_italic(strings.no_code())
        await message.reply(text, parse_mode=ParseMode.HTML)
        return

    m_text = html_italic(strings.running())
    m = await app.send_message(message.chat.id, m_text, ParseMode.HTML)

    result = await py_run(code, TIMEOUT, "p" not in args)
    await m.edit(result, ParseMode.HTML)
