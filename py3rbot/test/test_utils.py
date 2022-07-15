from typing import Optional
import pytest

from .. import utils, strings


@pytest.mark.parametrize("text,expected", [
    ("\n 3+4", ("3+4", "")),
    ("/pr 4+2", ("4+2", "pr")),
    ("/p\n /r\n  t + e", ("t + e", "pr")),
    ("/p    /p       /r", ("", "ppr")),
    ("x /y", ("x /y", "")),
    ("/1 / /2 / /x /$ n1 / n2", ("n1 / n2", "x")),
    ("   \n ", ("", "")),
])
def test_code_args_split(text: str, expected: tuple[str, str]):
    assert utils.code_args_split(text) == expected


@pytest.mark.parametrize("result,expected", [
    (None, f"<i>{strings.was_terminated()}</i>"),
    (" \n \n", f"<i>{strings.empty_output()}</i>"),
    ("toolong " * 1000, f"<i>{strings.too_long_output()}</i>"),
    ("x=3;x>2", "x=3;x&gt;2"),
])
def test_format_pyrun_result(result: Optional[str], expected: str):
    assert utils.format_pyrun_result(result) == expected
