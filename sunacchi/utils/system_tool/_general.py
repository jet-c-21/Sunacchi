# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/10/24
"""
import sys
import platform
import pathlib


def is_arm() -> bool:
    ret = False
    if "-arm" in platform.platform():
        ret = True
    return ret


def get_curr_process_work_root_dir() -> pathlib.Path:
    """
    Returns the working root directory of the current process using pathlib.
    """
    if hasattr(sys, 'frozen'):
        # If the program is frozen, return the parent directory of the executable
        return pathlib.Path(sys.executable).parent
    else:
        # Otherwise, return the current working directory
        return pathlib.Path.cwd()