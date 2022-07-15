from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.filters import command, private
from pyrogram.types import Message

from .. import strings
from ..constants import TIMEOUT
from ..filters import via_me
from ..pyrun import run_code
from ..utils import code_args_split, format_pyrun_result, html_italic


@Client.on_message(command("py")) # pyright: ignore
async def py_cmd(app: Client, message: Message) -> None:
    code, args = code_args_split(message.text.split(maxsplit=1)[1])
    await _send_result(app, message.chat.id, code, args)

@Client.on_message(private & ~via_me) # pyright: ignore
async def private_default(app: Client, message: Message) -> None:
    code, args = code_args_split(message.text)
    await _send_result(app, message.chat.id, code, args)

async def _send_result(app: Client, chat_id: int, code: str, args: str) -> None:
    if not code:
        text = html_italic(strings.no_code())
        await app.send_message(chat_id, text, ParseMode.HTML)
        return

    text = html_italic(strings.running())
    m = await app.send_message(chat_id, text, ParseMode.HTML)

    filename = "<%s>" % (await app.get_me()).username
    result = await run_code(code, filename, "p" not in args, TIMEOUT)
    result = format_pyrun_result(result)

    await m.edit(result, ParseMode.HTML)
