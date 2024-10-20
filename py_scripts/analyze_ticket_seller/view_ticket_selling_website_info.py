# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/20/24
"""
import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

import time
from pprint import pprint as pp

from sunacchi.utils.network_tool import (
    get_website_server_geo_location
)

import ipapi

if __name__ == '__main__':
    website_url = "https://tixcraft.com/"
    location_info = get_website_server_geo_location(website_url)

    for i in range(5):
        pp(location_info)
        print()
        time.sleep(1)

    # res = ipapi.location(ip='tixcraft.com')
    # print(res)
