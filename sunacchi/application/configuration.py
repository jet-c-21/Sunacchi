# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/23/24
"""
import platform
import pathlib
from typing import Dict

from sunacchi import var as VAR
from sunacchi.utils.file_tool import (
    read_json,
    create_file_from_template
)


def get_latest_settings_json_from_local(app_settings_file: pathlib.Path = None) -> Dict:
    if app_settings_file is None:
        app_settings_file = VAR.SETTINGS_FILE

    if not app_settings_file.is_file():
        create_file_from_template(app_settings_file, VAR.SETTINGS_TPL_FILE)
        msg = f"[*INFO*] - settings json file is not existed local, " \
              f"created settings file from template: {app_settings_file}"
        print(msg)

    settings = read_json(app_settings_file)

    return settings
