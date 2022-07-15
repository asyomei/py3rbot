import os
import sys
import pwd
from shutil import copytree
import subprocess

from ..getcurdir import getcurdir


try:
    pw = pwd.getpwnam("py3rbot")
    gid_uid = f"{pw.pw_gid} {pw.pw_uid}"
except KeyError:
    gid_uid = ""

if gid_uid and subprocess.call(["chroot", "/", "true"]) == 0:
    chroot = getcurdir(__file__) + "/chroot"
    python = chroot + "/python"
    if not os.path.isdir(chroot):
        os.mkdir(chroot)
    if not os.path.isdir(python):
        for path in sys.path:
            if "python3." in path and os.path.isdir(path):
                _ignore_site = lambda _, __: ["site-packages"]
                copytree(path, python, ignore=_ignore_site)
                break
        subprocess.check_call(["chmod", "0755", "-R", chroot])
else:
    chroot = python = ""
