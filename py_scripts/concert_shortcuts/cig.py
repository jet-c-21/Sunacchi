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

if __name__ == '__main__':
    settings_file = VAR.SETTINGS_FILE
    orig_json = get_latest_settings_json_from_local(settings_file)

    homepage = 'https://tixcraft.com/activity/detail/24_jaychou'
    orig_json['homepage'] = homepage

    to_json(orig_json, settings_file)

    wait_until_time(11, 59, 59, milliseconds=500)

    nodriver_py_script = PROJECT_DIR / 'nodriver_tixcraft.py'
    assert nodriver_py_script.is_file(), f"nodriver script not found: {nodriver_py_script}"

    # hwo to run this script in more fast way?
    Popen(['python3', str(nodriver_py_script), '--homepage', homepage])
