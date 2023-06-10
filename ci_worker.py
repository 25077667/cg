"""
A helper to multiplexing if the CI matrix environment.

If it is in Windows, it will execute windows script.
If it is in Linux, it will execute linux script. (Same as Mac OS, we call them unix-like system)

if the argc[1] is "lint", it will execute lint script.
! Test script is TBD
if the argc[1] is "build", it will execute build script.

- name: Check lint
run: |
# Use ./ci/check_lint to check lint
# Windows use ./ci/check_lint/windows.ps1 and unix(-like) use ./ci/check_lint/unix.sh


- name: Build with Nuitka
run: |
# Use ./ci/build_nuitka to build with Nuitka
# Windows use ./ci/build_nuitka/windows.ps1 and unix(-like) use ./ci/build_nuitka/unix.sh
"""

import os
import sys


def main(action: str) -> None:
    """
    Select script with the os and action.
    """
    ret_code = 0
    if os.name == 'nt':
        if action == "lint":
            ret_code = os.system("./ci/check_lint/windows.ps1")
        elif action == "build":
            ret_code = os.system("./ci/build_nuitka/windows.ps1")
    else:
        if action == "lint":
            ret_code = os.system("./ci/check_lint/unix.sh")
        elif action == "build":
            ret_code = os.system("./ci/build_nuitka/unix.sh")

    sys.exit(ret_code)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: the number of arguments is not 2")
        sys.exit(1)

    ACTION = ''
    if sys.argv[1] == "lint":
        ACTION += "lint"
    elif sys.argv[1] == "build":
        ACTION += "build"
    else:
        print("Error: the argument is not 'lint' or 'build'")
        sys.exit(1)

    main(ACTION)
