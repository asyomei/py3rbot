from html import escape as html_escape
from typing import Optional

from .. import strings
from ..constants import MAX_MESSAGE_TEXT_LENGTH
from ..pyrun import python_run_code


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


async def py_run(code: str,
                 timeout: Optional[float],
                 print_last_expr=True,
                 raw=False) -> str:
    result = await python_run_code(code, timeout, print_last_expr)
    return format_result(result) if not raw else result or ""


def format_result(result: Optional[str]) -> str:
    if result is None:
        return html_italic(strings.was_terminated())
    if not (result := result.strip()):
        return html_italic(strings.empty())
    if len(result) > MAX_MESSAGE_TEXT_LENGTH:
        return html_italic(strings.too_long_output())
    return html_escape(result)
