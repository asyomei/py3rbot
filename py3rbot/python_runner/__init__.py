from typing import Optional

from .python_runner import PythonAsyncRunner


_py = PythonAsyncRunner()


async def py_run(code: str, eval_mode: bool=False,
                 timeout: Optional[float]=None) -> Optional[str]:
    return await _py.run(code, eval_mode, timeout)


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
