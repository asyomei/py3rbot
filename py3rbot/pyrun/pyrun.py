from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import PIPE, create_subprocess_exec
from asyncio.tasks import wait_for
import sys
from typing import Optional

from ..getcurdir import getcurdir
from ._chroot import chroot, gid_uid


async def run_code(code: str, filename: str,
                   print_last_expr: bool, timeout: float) -> Optional[str]:
    args = _prepare_args(code, filename, print_last_expr)
    return await _subp_run(args, timeout)


def _prepare_args(code: str, filename: str,
                  print_last_expr: bool) -> list[str]:
    plexpr_flag = "1" if print_last_expr else ""
    py_argv = [chroot, gid_uid, plexpr_flag, filename, code]
    script = getcurdir(__file__) + "/__rc__.py"
    return [sys.executable, "-I", script] + py_argv


async def _subp_run(args: list[str], timeout: float) -> Optional[str]:
    p = await create_subprocess_exec(*args, stdout=PIPE, stderr=PIPE)

    try:
        out, err = await wait_for(p.communicate(), timeout)
    except AsyncioTimeoutError:
        p.terminate()
        await p.wait()
        return

    ok = p.returncode == 0
    buf = out if ok else err
    return buf.decode("utf-8")
