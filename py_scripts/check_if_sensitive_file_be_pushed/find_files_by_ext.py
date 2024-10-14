# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/14/24
"""
import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from sunacchi.utils.file_tool import read_json, create_dir, to_json

if __name__ == '__main__':
    tpl_dir = PROJECT_DIR / 'settings-templates'
    web_ui_json_template_file = tpl_dir / 'settings.json'

    web_ui_json = read_json(web_ui_json_template_file)

    msg = f"web ui json keys: {web_ui_json.keys()}"
    print(msg)

    ext_dir = PROJECT_DIR / 'webdriver'

    maxbot_ext_dir = ext_dir / 'Maxbotplus_1.0.0'
    maxbot_ext_data_dir = maxbot_ext_dir / 'data'
    maxbot_ext_json_path = maxbot_ext_data_dir / 'settings.json'
    maxbot_ext_json = read_json(maxbot_ext_json_path)

    msg = f"maxbot ext json keys: {maxbot_ext_json.keys()}"
    print(msg)

    maxblock_ext_dir = ext_dir / 'Maxblockplus_1.0.0'
    maxblock_ext_data_dir = maxblock_ext_dir / 'data'
    maxblock_ext_json_path = maxblock_ext_data_dir / 'settings.json'

    maxblock_ext_json = read_json(maxblock_ext_json_path)

    msg = f"maxblock ext json keys: {maxblock_ext_json.keys()}"
    print(msg)

    print(web_ui_json.keys() == maxbot_ext_json.keys())

    print(maxbot_ext_json.keys() == maxblock_ext_json.keys())

    browser_ext_tpl_root_dir = tpl_dir / 'browser_extensions'

    maxbot_ext_name = 'Maxbotplus_1.0.0'
    maxbot_ext_tpl_dir = browser_ext_tpl_root_dir / maxbot_ext_name
    create_dir(maxbot_ext_tpl_dir)
    maxbot_ext_tpl_json_path = maxbot_ext_tpl_dir / 'settings.json'
    to_json(
        maxbot_ext_json, maxbot_ext_tpl_json_path
    )

    maxblock_ext_name = 'Maxblockplus_1.0.0'
    maxblock_ext_tpl_dir = browser_ext_tpl_root_dir / maxblock_ext_name
    create_dir(maxblock_ext_tpl_dir)
    maxblock_ext_tpl_json_path = maxblock_ext_tpl_dir / 'settings.json'
    to_json(
        maxblock_ext_json, maxblock_ext_tpl_json_path
    )
