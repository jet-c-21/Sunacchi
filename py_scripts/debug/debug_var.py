# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/21/24
"""
import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from sunacchi import var as VAR

from sunacchi.utils.log_tool import (
    create_logger,
    get_cls_instance_logger
)

if __name__ == '__main__':
    print(f"VAR.SUNACCHI_PY_PKG_DIR: {VAR.SUNACCHI_PY_PKG_DIR}")
    print(f"VAR.PROJECT_DIR: {VAR.PROJECT_DIR}")
