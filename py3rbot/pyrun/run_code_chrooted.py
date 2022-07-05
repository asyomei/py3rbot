import ast
import os
import pwd
import sys
from traceback import format_exception
from typing import Any


def tb_exec(compiled: Any, globals: dict[str, Any]) -> None:
    try:
        exec(compiled, globals)
    except Exception as exc:
        fmt = format_exception(exc)
        fmt.pop(1)
        print("".join(fmt))
        sys.exit(1)


def tb_eval(compiled: Any, globals: dict[str, Any]) -> Any:
    try:
        return eval(compiled, globals)
    except Exception as exc:
        fmt = format_exception(exc)
        fmt.pop(1)
        print("".join(fmt))
        sys.exit(1)


def exec_with_ret_last_expr(code: str) -> Any:
    mod = ast.parse(code)

    if not mod.body:
        return

    file = "<string>"
    globals = {"__builtins__": __builtins__}

    last_expr = mod.body[-1]
    if type(last_expr) is not ast.Expr:
        tb_exec(compile(mod, file, "exec"), globals)
        return

    mod.body = mod.body[:-1]
    if mod.body:
        tb_exec(compile(mod, file, "exec"), globals)
    expr = ast.Expression(last_expr.value)
    return tb_eval(compile(expr, file, "eval"), globals)


def chuser(pw: pwd.struct_passwd) -> None:
    os.setgid(pw.pw_gid)
    os.setuid(pw.pw_uid)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(1)

    pw = pwd.getpwnam("py3rbot")
    chroot_dir = os.path.dirname(os.path.realpath(__file__)) + "/chroot"
    os.chroot(chroot_dir)
    chuser(pw)
    sys.path = ["/python"]

    value = exec_with_ret_last_expr(sys.argv[2])
    if int(sys.argv[1]) and value is not None:
        print(value)
