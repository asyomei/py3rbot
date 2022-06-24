from .python_runner import PythonRunner


def from_eval(expr: str) -> str:
    modules = "import math, random"
    code = f"compile({expr!r},'<eval>','eval')"
    return f"{modules};print(eval({code}))"
