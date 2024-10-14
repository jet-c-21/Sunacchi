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


def dump_settings_to_maxbot_plus_extension(ext_dir: Union[str, pathlib.Path],
                                           config_dict: Dict,
                                           ext_config_file_name: str):
    # sync config.
    target_path = ext_dir
    target_path = os.path.join(target_path, "data")
    target_path = os.path.join(target_path, ext_config_file_name)
    # print("save as to:", target_path)

    # clear existed file
    if os.path.isfile(target_path):
        try:
            # print("remove file:", target_path)
            os.unlink(target_path)
        except Exception as e:
            pass

    # overwrite file
    try:
        with open(target_path, 'w') as outfile:
            json.dump(config_dict, outfile)
    except Exception as e:
        pass

    # add host_permissions
    target_path = ext_dir
    target_path = os.path.join(target_path, "manifest.json")

    manifest_dict = None
    if os.path.isfile(target_path):
        try:
            with open(target_path) as json_data:
                manifest_dict = json.load(json_data)
        except Exception as e:
            pass

    local_remote_url_array = []
    local_remote_url = config_dict["advanced"]["remote_url"]
    if len(local_remote_url) > 0:
        try:
            temp_remote_url_array = json.loads("[" + local_remote_url + "]")
            for remote_url in temp_remote_url_array:
                remote_url_final = remote_url + "*"
                local_remote_url_array.append(remote_url_final)
        except Exception as e:
            pass

    if len(local_remote_url_array) > 0:
        is_manifest_changed = False
        if 'host_permissions' in manifest_dict:
            for remote_url_final in local_remote_url_array:
                if not remote_url_final in manifest_dict["host_permissions"]:
                    # print("local remote_url not in manifest:", remote_url_final)
                    manifest_dict["host_permissions"].append(remote_url_final)
                    is_manifest_changed = True

        if is_manifest_changed:
            json_str = json.dumps(manifest_dict, indent=4)
            try:
                with open(target_path, 'w') as outfile:
                    outfile.write(json_str)
            except Exception as e:
                pass
