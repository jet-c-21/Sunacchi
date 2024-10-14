# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/14/24
"""
from typing import Union, Dict, List
import os
import pathlib

from sunacchi.utils.file_tool import to_json


def dump_settings_to_maxblock_plus_extension(ext_dir: Union[str, pathlib.Path],
                                             config_dict: Dict,
                                             ext_config_file_name: str,
                                             block_domain_ls: List[str]):
    # sync config.
    target_path = ext_dir
    target_path = os.path.join(target_path, "data")
    # special case, due to data folder is empty, sometime will be removed.
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    target_path = os.path.join(target_path, ext_config_file_name)
    # print("save as to:", target_path)

    # deleted existed file
    if os.path.isfile(target_path):
        try:
            # print("remove file:", target_path)
            os.unlink(target_path)
        except Exception as e:
            pass

    config_dict["domain_filter"] = block_domain_ls
    try:
        to_json(config_dict, target_path)
    except Exception as e:
        pass
