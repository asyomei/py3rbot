from typing import Callable

from .. import strings
from ..strings import dict


def test_strings():
    for name, var in vars(strings).items():
        if not isinstance(var, Callable):
            continue

        key = name.replace("_", "-")
        val = dict._dict.get(key)

        assert val is not None, f"No string with key {key!r}"

        args = [""] * var.__code__.co_argcount
        try:
            _ = var(*args)
        except KeyError as err:
            err.args = f"Missing format key {err} in string {key!r}",
            raise
