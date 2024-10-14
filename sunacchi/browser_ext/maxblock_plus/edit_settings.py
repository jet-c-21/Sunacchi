# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/14/24
"""
from typing import Union, Dict
import json
import os
import pathlib


def dump_settings_to_maxblock_plus_extension(ext_dir: Union[str, pathlib.Path],
                                             config_dict: Dict,
                                             ext_config_file_name:str,
                                             CONST_MAXBLOCK_EXTENSION_FILTER):
    # sync config.
    target_path = ext_dir
    target_path = os.path.join(target_path, "data")
    # special case, due to data folder is empty, sometime will be removed.
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    target_path = os.path.join(target_path, ext_config_file_name)
    # print("save as to:", target_path)
    if os.path.isfile(target_path):
        try:
            # print("remove file:", target_path)
            os.unlink(target_path)
        except Exception as exc:
            pass

    try:
        with open(target_path, 'w') as outfile:
            config_dict["domain_filter"] = CONST_MAXBLOCK_EXTENSION_FILTER
            json.dump(config_dict, outfile)
    except Exception as e:
        pass
