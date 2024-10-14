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

from sunacchi.utils.file_tool import (
    find_all_files_with_ext
)

if __name__ == '__main__':
    find_all_files_with_ext(PROJECT_DIR, '.json')

    # find_all_files_with_ext(PROJECT_DIR, '.txt')

    # find_all_files_with_ext(PROJECT_DIR, '.crx')
