import html

from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.handlers.handler import Handler
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types.inline_mode import (
    ChosenInlineResult,
    InlineQuery,
    InlineQueryResultArticle,
)
from pyrogram.types.input_message_content import InputTextMessageContent

from .. import strings
from ..constants import TIMEOUT
from ..python_runner import PythonRunner, code_args_split, from_eval
from .handler_decorator import on_chosen_inline_result, on_inline_query
from .utils import get_formatted, html_italic


handlers = list[tuple[Handler, int]]()
on_chosen_inline_result = on_chosen_inline_result(handlers)
on_inline_query = on_inline_query(handlers)


@on_inline_query()
async def inline_query_handler(_: Client, query: InlineQuery) -> None:
    code = code_args_split(query.query)[0]

    if not code:
        await query.answer([])
        return

    btn = InlineKeyboardButton(strings.running, "0")
    markup = InlineKeyboardMarkup([[btn]])

    result_article = InlineQueryResultArticle(
        title=strings.run_code,
        description=code,
        reply_markup=markup,
        input_message_content=InputTextMessageContent(query.query),
        thumb_url="https://www.python.org/static/opengraph-icon-200x200.png",
    )

    await query.answer([result_article], cache_time=0)


@on_chosen_inline_result()
async def chosen_inline_result_handler(app: Client,
                                       chosen: ChosenInlineResult) -> None:
    code, args = code_args_split(chosen.query)

    if "e" in args:
        code = from_eval(code)

    result = await PythonRunner.run(code, TIMEOUT)
    result = get_formatted(result)

    text = ""
    if "r" not in args:
        text += html.escape(code)
        text += f"\n\n--- {html_italic(strings.output)} ---\n\n"

    inline_id = chosen.inline_message_id
    try:
        await app.edit_inline_text(inline_id, text + result, ParseMode.HTML)
    except MessageTooLong:
        result = html_italic(strings.too_long_output)
        await app.edit_inline_text(inline_id, text + result, ParseMode.HTML)
