# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/23/24
"""
import pathlib

_THIS_FILE_PATH = pathlib.Path(__file__).absolute()
_THIS_FILE_PARENT_DIR = _THIS_FILE_PATH.parent
SUNACCHI_PY_PKG_DIR = _THIS_FILE_PARENT_DIR.parent
PROJECT_DIR = SUNACCHI_PY_PKG_DIR.parent

SETTINGS_TEMPLATES_DIR = PROJECT_DIR / 'settings-templates'
SETTINGS_TPL_FILE = SETTINGS_TEMPLATES_DIR / 'settings.json'

LOG_DIR = PROJECT_DIR / 'logs'

SETTINGS_FILE = PROJECT_DIR / SETTINGS_TPL_FILE.name
