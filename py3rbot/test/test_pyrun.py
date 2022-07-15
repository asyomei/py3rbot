from typing import Optional
import asyncio
import pytest

from ..pyrun import run_code


print_error = """File "<pytest>", line 1
    print 12
    ^^^^^^^^
SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?"""

x_is_not_defined = """Traceback (most recent call last):
  File "<pytest>", line 1, in <module>
NameError: name 'x' is not defined"""

type_error = """Traceback (most recent call last):
  File "<pytest>", line 3, in <module>
TypeError: unsupported operand type(s) for /: 'int' and 'str'"""


@pytest.mark.parametrize("code,prlastexpr,expected", [
    (" \n ", True, ""),
    ("print(12)", True, "12"),
    ("print 12", True, print_error),
    ("x=5;y=7\nx+y", True, "12"),
    ("x=6\nx * x", False, ""),
    ("x = 6\nprint(x ** 2)", True, "36"),
    ("print(x + y)", False, x_is_not_defined),
    ("x = 5\ny = 'q'\nx / y", True, type_error),
])
def test_run_code(code: str, prlastexpr: bool, expected: Optional[str]):
    result = asyncio.run(run_code(code, "<pytest>", prlastexpr, 5))
    if result is not None:
        result = result.replace("# Warning! Unsafe", "").strip()
    assert result == expected
