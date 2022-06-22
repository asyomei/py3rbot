from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import PIPE, create_subprocess_exec
from asyncio.tasks import wait_for
from os import path
from pwd import getpwnam
from subprocess import CalledProcessError, check_call
from traceback import format_exc
from typing import Optional


CHROOT = ""
try:
    pw = getpwnam("py3rbot")
    check_call(["chroot", "/", "true"])
    CHROOT = path.dirname(path.realpath(__file__)) + "/chroot"
    CHROOT = (
        f"__import__('os').chroot('{CHROOT}')\n"
        f"__import__('os').setgid({pw.pw_gid})\n"
        f"__import__('os').setuid({pw.pw_uid})\n"
         "__import__('sys').path=['/python']\n"
    )
except KeyError:
    print("Error! not found py3rbot user, not safe")
    if input("Continue? y/n: ").lower() != "y":
        raise InterruptedError
except CalledProcessError:
    print("Error! chroot command was return non-zero code, not safe")
    if input("Continue? y/n: ").lower() != "y":
        raise InterruptedError


class PythonAsyncRunner:
    async def run(self, code: str, eval_mode: bool=False,
                  timeout: Optional[float]=None) -> Optional[str]:
        if err := self._check(code, eval_mode):
            return err

        if eval_mode:
            code = f"import math;print({code})"
        args = ["python", "-Ic", CHROOT + code]
        return await self._subp_run(args, timeout)


    def _check(self, code: str, eval_mode: bool) -> Optional[str]:
        mode = "eval" if eval_mode else "exec"
        try:
            compile(code, "<check>", mode)
        except SyntaxError:
            return "Traceback (most recent call last):\n" + format_exc(0)


    async def _subp_run(self, args: list[str],
                        timeout: Optional[float]) -> Optional[str]:
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
