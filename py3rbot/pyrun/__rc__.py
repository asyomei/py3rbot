import ast
import sys
from traceback import format_exception

def throw_error(err, i, n):
    tb = format_exception(err)
    for _ in range(n): del tb[i]
    msg = "".join(tb)
    sys.stderr.write(msg)
    sys.exit(1)

def tb_parse(code, filename):
    try:
        return ast.parse(code, filename)
    except SyntaxError as err:
        throw_error(err, 0, 3)

def tb_exec(mod, filename, globals):
    try:
        exec(compile(mod, filename, "exec"), globals)
    except Exception as exc:
        throw_error(exc, 1, 1)

def tb_eval(expr, filename, globals):
    try:
        return eval(compile(expr, filename, "eval"), globals)
    except Exception as exc:
        throw_error(exc, 1, 1)

def exec_ret_last_expr(code, filename):
    mod = tb_parse(code, filename)
    if not mod.body: return
    globals = {"__builtins__": __builtins__}
    last_expr = None
    if isinstance(mod.body[-1], ast.Expr):
        *mod.body, last_expr = mod.body
    if mod.body: tb_exec(mod, filename, globals)
    if last_expr:
        expr = ast.Expression(last_expr.value)
        return tb_eval(expr, filename, globals)

chroot = sys.argv[1]
gid_uid = sys.argv[2]
print_last_expr = sys.argv[3]
filename = sys.argv[4]
code = sys.argv[5]

if chroot:
    gid, uid = map(int, gid_uid.split())
    import os
    os.chroot(chroot)
    os.setgid(gid)
    os.setuid(uid)
    sys.path = ["/python"]
else:
    msg = "# Warning! Unsafe\n"
    sys.stdout.write(msg)
    sys.stderr.write(msg)

value = exec_ret_last_expr(code, filename)
if value is not None and print_last_expr:
    print(value)
