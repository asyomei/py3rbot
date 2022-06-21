import html
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

    return html.escape(result)


def html_italic(text: str) -> str:
    return f"<i>{html.escape(text)}</i>"
