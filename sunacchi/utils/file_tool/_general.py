# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/10/24
"""
from typing import Union, Dict, List
from argparse import Namespace
import json
import os
import pathlib
import shutil


def create_dir(dir_path: Union[pathlib.Path, str],
               parents=True,
               exist_ok=True) -> pathlib.Path:
    dir_path = pathlib.Path(dir_path)
    if not dir_path.is_dir():
        dir_path.mkdir(parents=parents, exist_ok=exist_ok, mode=0o777)
        dir_path.chmod(0o777)

    return dir_path


def str_ls_to_txt_file(str_ls: List, fp: Union[pathlib.Path, str]) -> pathlib.Path:
    fp = pathlib.Path(fp)
    with open(fp, 'w', encoding='utf-8') as f:
        for s in str_ls:
            f.write(str(s) + '\n')
    return fp


def txt_file_to_str_ls(fp: Union[pathlib.Path, str]) -> List:
    with open(fp, 'r', encoding='utf-8') as f:
        str_ls = [line.strip() for line in f.readlines()]
    return str_ls


def to_json(data: Union[Dict, Namespace, List],
            fp: Union[str, pathlib.Path]) -> pathlib.Path:
    fp = pathlib.Path(fp)
    if not fp.parent.is_dir():
        fp.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, Namespace):
        data = vars(data)

    json.dump(
        data,
        open(fp, 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )
    fp.chmod(0o777)

    return fp


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


def find_all_files_with_ext(root_dir: pathlib.Path, file_ext: str) -> List[pathlib.Path]:
    """
    Finds all files with the specified extension in the given root directory and its subdirectories.

    :param root_dir: The root directory to search for files.
    :param file_ext: The file extension to search for (e.g., '.txt').
    :return: A list of Paths representing all files found with the specified extension.
    """
    matched_f_ls = list(root_dir.rglob(f'*{file_ext}'))

    if matched_f_ls:
        msg = f"[*INFO*] - found {len(matched_f_ls)} {file_ext} files in {root_dir}:"
        print(msg)
        for f in matched_f_ls:
            print(f)
        print()

    else:
        msg = f"[*INFO*] - None of {file_ext} file found in {root_dir}"
        print(msg)

    return matched_f_ls


def chmod_777(fp: Union[pathlib.Path, str]):
    fp = pathlib.Path(fp)
    if fp.exists():
        fp.chmod(0o777)
