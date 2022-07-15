from .dict import get as _get


def start_message():
    return _get(start_message)

def help_message(python_version: str):
    return _get(help_message, python_version=python_version)

def py_message():
    return _get(py_message)

def inline_message(botname: str):
    return _get(inline_message, botname=botname)

def empty_output():
    return _get(empty_output)

def too_long_output():
    return _get(too_long_output)

def was_terminated():
    return _get(was_terminated)

def output():
    return _get(output)

def no_code():
    return _get(no_code)

def run_code():
    return _get(run_code)

def running():
    return _get(running)

def too_long_query():
    return _get(too_long_query)
