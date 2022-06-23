from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import PIPE, create_subprocess_exec
from asyncio.tasks import wait_for
from os import path
from pwd import getpwnam
from subprocess import CalledProcessError, check_call
from traceback import format_exc
from typing import Optional


CHROOT = "{}"
try:
    pw = getpwnam("py3rbot")
    check_call(["chroot", "/", "true"])
    CHROOT = path.dirname(path.realpath(__file__)) + "/chroot"
    CHROOT = (
        f"__import__('os').chroot('{CHROOT}')\n"
        f"__import__('os').setgid({pw.pw_gid})\n"
        f"__import__('os').setuid({pw.pw_uid})\n"
         "__import__('sys').path=['/python']\n"
         "exec(compile({!r},'<exec>','exec'))"
    )
except KeyError:
    print("Error! not found py3rbot user, not safe")
    if input("Continue? y/n: ").lower() != "y":
        raise InterruptedError
except CalledProcessError:
    print("Error! chroot command was return non-zero code, not safe")
    if input("Continue? y/n: ").lower() != "y":
        raise InterruptedError


class PythonRunner:
    @staticmethod
    async def run(code: str, timeout: Optional[float]=None) -> Optional[str]:
        if err := PythonRunner._check(code):
            return err
        args = ["python", "-Ic", CHROOT.format(code)]
        return await PythonRunner._subp_run(*args, timeout=timeout)


    @staticmethod
    def _check(code: str) -> Optional[str]:
        try:
            compile(code, "<check>", "exec")
        except SyntaxError:
            return "Traceback (most recent call last):\n" + format_exc(0)


    @staticmethod
    async def _subp_run(*args: str, timeout: Optional[float]) -> Optional[str]:
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
