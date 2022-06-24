from html import escape as html_escape
from typing import Optional

from .. import strings
from ..constants import MAX_MESSAGE_TEXT_LENGTH


def get_formatted(result: Optional[str]) -> str:
    if result is None:
        return html_italic(strings.was_terminated())

    result = result.strip()

    if not result:
        return html_italic(strings.empty())

    if len(result) > MAX_MESSAGE_TEXT_LENGTH:
        return html_italic(strings.too_long_output())

    return html_escape(result)


def html_italic(text: str) -> str:
    return f"<i>{html_escape(text)}</i>"


def code_args_split(text: str) -> tuple[str, str]:
    if not text:
        return "", ""

    args = ""

    while True:
        arg, *new_text = text.split(maxsplit=1)

        if not arg.startswith("/"):
            return text, args

        args += "".join(filter(str.isalpha, arg))

        if not new_text:
            return "", args

        text ,= new_text
