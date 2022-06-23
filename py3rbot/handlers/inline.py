from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.filters import Filter, create as create_filter
from pyrogram.handlers.handler import Handler
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types.inline_mode import (
    ChosenInlineResult,
    InlineQuery,
    InlineQueryResultArticle,
)
from pyrogram.types.input_message_content import InputTextMessageContent

from .. import strings
from ..constants import MAX_INLINE_QUERY_LENGTH, TIMEOUT
from ..python_runner import PythonRunner, code_args_split, from_eval
from .handler_decorator import on_chosen_inline_result, on_inline_query
from .utils import get_formatted, html_escape, html_italic


handlers = list[tuple[Handler, int]]()
on_chosen_inline_result = on_chosen_inline_result(handlers)
on_inline_query = on_inline_query(handlers)


@create_filter
async def inline_message_id(_: Filter, __: Client,
                            chosen: ChosenInlineResult) -> bool:
    return not not chosen.inline_message_id


@on_inline_query()
async def inline_query_handler(_: Client, query: InlineQuery) -> None:
    code = code_args_split(query.query)[0]

    if not code:
        text = html_italic(strings.no_code())
        await query.answer([InlineQueryResultArticle(
            id="no_code",
            title=strings.no_code(),
            input_message_content=InputTextMessageContent(text, ParseMode.HTML)
        )])
        return

    if len(query.query) >= MAX_INLINE_QUERY_LENGTH:
        text = html_italic(strings.too_long_query())
        await query.answer([InlineQueryResultArticle(
            id="too_long_query",
            title=strings.too_long_query(),
            input_message_content=InputTextMessageContent(text, ParseMode.HTML)
        )])
        return

    btn = InlineKeyboardButton(strings.running(), "0")
    result_article = InlineQueryResultArticle(
        title=strings.run_code(),
        description=code,
        reply_markup=InlineKeyboardMarkup([[btn]]),
        input_message_content=InputTextMessageContent(query.query),
        thumb_url="https://www.python.org/static/opengraph-icon-200x200.png",
    )
    await query.answer([result_article], cache_time=0)


@on_chosen_inline_result(inline_message_id)
async def chosen_inline_result_handler(app: Client,
                                       chosen: ChosenInlineResult) -> None:
    code, args = code_args_split(chosen.query)

    old_code = code
    if eval_mode := "e" in args:
        code = from_eval(code)

    result = await PythonRunner.run(code, TIMEOUT)
    result = get_formatted(result)

    text = ""
    if "r" not in args:
        if eval_mode:
            code = "# eval mode\n" + old_code
        text += html_escape(code)
        text += f"\n\n--- {html_italic(strings.output())} ---\n\n"

    inline_id = chosen.inline_message_id
    try:
        await app.edit_inline_text(inline_id, text + result, ParseMode.HTML)
    except MessageTooLong:
        result = html_italic(strings.too_long_output())
        await app.edit_inline_text(inline_id, text + result, ParseMode.HTML)
