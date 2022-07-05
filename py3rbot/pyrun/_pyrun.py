from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import PIPE, create_subprocess_exec
from asyncio.tasks import wait_for
import os
from shutil import copytree
import subprocess
import sys
from typing import Optional


curdir = os.path.dirname(os.path.realpath(__file__))
has_chroot = subprocess.call(["chroot", "/", "true"]) == 0

if not has_chroot:
    print("Unsafe")


async def python_run_code(code: str,
                          timeout: Optional[float],
                          print_last_expr: bool) -> Optional[str]:
    args = _prepare_args(code, print_last_expr)
    return await _subp_run(args, timeout)


def _prepare_args(code: str, print_last_expr: bool) -> list[str]:
    print_last_expr_flag = "1" if print_last_expr else "0"
    chroot_file = "_chrooted" if has_chroot else ""
    script = curdir + f"/run_code{chroot_file}.py"
    return [sys.executable, "-I", script, print_last_expr_flag, code]


async def _subp_run(args: list[str], timeout: Optional[float]) -> Optional[str]:
    p = await create_subprocess_exec(*args, stdout=PIPE, stderr=PIPE)

    try:
        out, err = await wait_for(p.communicate(), timeout)
    except AsyncioTimeoutError:
        p.terminate()
        await p.wait()
        return

    ok = p.returncode == 0
    buf = out if ok else err
    return buf.decode()


chroot_dir = curdir + "/chroot"
python_dir = chroot_dir + "/python"

if has_chroot and not os.path.isdir(python_dir):
    if not os.path.isdir(chroot_dir):
        os.mkdir(chroot_dir)
    for path in sys.path:
        if "python" in path and os.path.isdir(path):
            copytree(path, python_dir)
            break
    subprocess.check_call(["chmod", "0755", "-R", chroot_dir])
