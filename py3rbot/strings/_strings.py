from typing import Callable as _Callable, Any as _Any
from yaml import safe_load as _yaml_load
from os import path as _path


_yaml_file = _path.dirname(_path.realpath(__file__)) + "/strings.yaml"


with open(_yaml_file, "r") as _yaml_file:
    _dict: dict[str, str] = _yaml_load(_yaml_file)


def _get(func: _Callable[..., str], **kwargs: _Any) -> str:
    key = func.__name__.replace("_", "-")
    str = _dict[key].strip()
    return str.format_map(kwargs)


# -- strings --

def start() -> str:
    return _get(start)

def help(python_version: str) -> str:
    return _get(help, python_version=python_version)


def py_cmd_help() -> str:
    return _get(py_cmd_help)

def inline_help(botname: str) -> str:
    return _get(inline_help, botname=botname)


def empty() -> str:
    return _get(empty)

def too_long_output() -> str:
    return _get(too_long_output)

def was_terminated() -> str:
    return _get(was_terminated)


def output() -> str:
    return _get(output)

def no_code() -> str:
    return _get(no_code)

def run_code() -> str:
    return _get(run_code)

def running() -> str:
    return _get(running)

def too_long_query() -> str:
    return _get(too_long_query)
