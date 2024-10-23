# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/23/24
"""
import platform
import pathlib

from sunacchi import var as VAR
from sunacchi.utils.file_tool import (
    read_json,
    create_file_from_template
)


def get_application_timezone(app_settings_file: pathlib.Path = None) -> str:
    if app_settings_file is None:
        app_settings_file = VAR.SETTINGS_FILE

    if not app_settings_file.is_file():
        create_file_from_template(app_settings_file, VAR.SETTINGS_TPL_FILE)

    settings = read_json(app_settings_file)

    return settings.get('application_timezone', 'Asia/Taipei')



