from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import (
    ChosenInlineResult,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from .. import strings
from ..constants import MAX_INLINE_QUERY_LENGTH, TIMEOUT
from ..utils import code_args_split, html_escape, html_italic, py_run


@Client.on_inline_query() # type: ignore
async def inline_no_code(_, query: InlineQuery) -> None:
    if code_args_split(query.query)[0]:
        query.continue_propagation()

    result = InlineQueryResultArticle(
        id="no-code",
        title=strings.no_code(),
        input_message_content=InputTextMessageContent(
            html_italic(strings.no_code()),
            parse_mode=ParseMode.HTML
        )
    )
    await query.answer([result])


@Client.on_inline_query() # type: ignore
async def inline_too_long_query(_, query: InlineQuery) -> None:
    if len(query.query) < MAX_INLINE_QUERY_LENGTH:
        query.continue_propagation()

    result = InlineQueryResultArticle(
        id="too-long",
        title=strings.too_long_query(),
        input_message_content=InputTextMessageContent(
            html_italic(strings.too_long_query()),
            parse_mode=ParseMode.HTML
        )
    )
    await query.answer([result], cache_time=0)


@Client.on_inline_query() # type: ignore
async def inline_query_default_handler(_, query: InlineQuery) -> None:
    code = code_args_split(query.query)[0]

    result = InlineQueryResultArticle(
        id=query.id,
        title=strings.run_code(),
        description=code,
        input_message_content=InputTextMessageContent(query.query),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(strings.running(), callback_data="0")
        ]])
    )
    await query.answer([result], cache_time=0)


@Client.on_chosen_inline_result() # type: ignore
async def chosen_no_inline_message(_, chosen: ChosenInlineResult) -> None:
    if chosen.inline_message_id:
        chosen.continue_propagation()


@Client.on_chosen_inline_result() # type: ignore
async def on_chosen_inline_result(app: Client, chosen: ChosenInlineResult) -> None:
    code, args = code_args_split(chosen.query)

    result = await py_run(code, TIMEOUT, "p" not in args)

    output = ""
    if "r" not in args:
        output = html_escape(code)
        output += f"\n\n--- {html_italic(strings.output())} ---\n\n"
    text = output + result

    try:
        await app.edit_inline_text(chosen.inline_message_id, text, ParseMode.HTML)
    except MessageTooLong:
        text = output + html_italic(strings.too_long_output())
        await app.edit_inline_text(chosen.inline_message_id, text, ParseMode.HTML)
