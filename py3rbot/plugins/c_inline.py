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
from ..pyrun import run_code
from ..utils import code_args_split, format_pyrun_result, html_escape, html_italic


@Client.on_inline_query() # pyright: ignore
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

@Client.on_inline_query() # pyright: ignore
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
    await query.answer([result])

@Client.on_inline_query() # pyright: ignore
async def inline_default(_, query: InlineQuery) -> None:
    result = InlineQueryResultArticle(
        id=query.id,
        title=strings.run_code(),
        description=code_args_split(query.query)[0],
        input_message_content=InputTextMessageContent(query.query),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(strings.running(), callback_data="0")
        ]])
    )
    await query.answer([result], cache_time=0)


@Client.on_chosen_inline_result() # pyright: ignore
async def chosen_no_inline_id(_, chosen: ChosenInlineResult) -> None:
    if chosen.inline_message_id:
        chosen.continue_propagation()

@Client.on_chosen_inline_result() # pyright: ignore
async def chosen_default(app: Client, chosen: ChosenInlineResult) -> None:
    inline_id = chosen.inline_message_id
    code, args = code_args_split(chosen.query)

    filename = "<%s>" % (await app.get_me()).username
    result = await run_code(code, filename, "p" not in args, TIMEOUT)
    result = format_pyrun_result(result)

    text = ""
    if "r" not in args:
        output = html_italic(strings.output())
        text = html_escape(code)
        text += f"\n\n --- {output} --- \n\n"

    try:
        message_text = text + result
        await app.edit_inline_text(inline_id, message_text, ParseMode.HTML)
    except MessageTooLong:
        result = html_italic(strings.too_long_output())
        message_text = text + result
        await app.edit_inline_text(inline_id, message_text, ParseMode.HTML)
