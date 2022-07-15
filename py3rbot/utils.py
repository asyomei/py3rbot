from html import escape as html_escape
from typing import Optional

from . import strings
from .constants import MAX_MESSAGE_TEXT_LENGTH


def html_italic(text: str, escape=True) -> str:
    if escape: text = html_escape(text)
    return f"<i>{text}</i>"


def code_args_split(text: str) -> tuple[str, str]:
    if not (text := text.strip()):
        return "", ""

    args = ""

    while True:
        arg, *sub = text.split(maxsplit=1)
        if not arg.startswith("/"):
            return text, args
        args += "".join(filter(str.isalpha, arg))
        if not sub:
            return "", args
        text ,= sub


def format_pyrun_result(result: Optional[str]) -> str:
    if result is None:
        return html_italic(strings.was_terminated())
    if not (result := result.strip()):
        return html_italic(strings.empty_output())
    if len(result) > MAX_MESSAGE_TEXT_LENGTH:
        return html_italic(strings.too_long_output())
    return html_escape(result)
