# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/10/24
"""
import json
from typing import Union, Dict, List
import os
import pathlib


def read_json(fp: Union[pathlib.Path, str]) -> Union[Dict, List]:
    fp = pathlib.Path(fp)
    assert fp.is_file(), f"input file is not existed: {fp}"
    return json.load(open(fp, 'r', encoding='utf-8'))


def create_file_from_template(target_file_path: Union[pathlib.Path, str],
                              template_file_path: Union[pathlib.Path, str],
                              chmod777_for_first_parent=True) -> pathlib.Path:
    target_file_path = pathlib.Path(target_file_path)
    if target_file_path.is_file():
        # If the file already exists, return its path without modification
        return target_file_path

    # Create the parent directory if it doesn't exist
    if not target_file_path.parent.exists():
        target_file_path.parent.mkdir(parents=True, exist_ok=True)
        if chmod777_for_first_parent:
            # Change the permission of the first parent directory, if required
            os.chmod(target_file_path.parent, 0o777)

    # Copy the template file to the target location
    template_file_path = pathlib.Path(template_file_path)
    shutil.copy(template_file_path, target_file_path)

    # Change the permission of the newly created file to make it modifiable by any user
    target_file_path.chmod(0o777)

    return target_file_path
