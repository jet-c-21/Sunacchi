# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/23/24
"""
import pathlib
import sys

# add project directory to path
THIS_FILE_PATH = pathlib.Path(__file__).absolute()
THIS_FILE_PARENT_DIR = THIS_FILE_PATH.parent
PROJECT_DIR = THIS_FILE_PARENT_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from sunacchi import var as VAR
from subprocess import Popen

from sunacchi.utils import wait_until_time
from sunacchi.application import get_application_timezone, get_latest_settings_json_from_local
from sunacchi.utils.file_tool import (
    read_json,
    to_json,
)
from sunacchi.utils.system_tool import curr_machine_is_gcp_vm

if __name__ == '__main__':
    is_gcp_vm = curr_machine_is_gcp_vm()
    print(f"[INFO] - is gcp vm: {is_gcp_vm}")
