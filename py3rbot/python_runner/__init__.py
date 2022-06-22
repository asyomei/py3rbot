from .python_runner import PythonRunner


def from_eval(expr: str) -> str:
    modules = "import math, random"
    return f"{modules}\nexpr = eval({expr!r})\nprint(expr)"


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
