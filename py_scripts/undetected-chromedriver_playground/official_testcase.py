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

from sunacchi.utils.file_tool import txt_file_to_str_ls

import time
import undetected_chromedriver as uc


if __name__ == '__main__':
    free_proxy_ls_txt_file = PROJECT_DIR / 'proxy_servers_files' / 'free-proxy-list.txt'
    assert free_proxy_ls_txt_file.is_file(), f"File not found: {free_proxy_ls_txt_file}"
    free_proxy_ls = txt_file_to_str_ls(free_proxy_ls_txt_file)

    # for proxy in free_proxy_ls:
    #     options = uc.ChromeOptions()
    #     options.add_argument(f'--proxy-server=http://{proxy}')
    #
    #     driver = uc.Chrome(options=options, use_subprocess=False)
    #     driver.get('https://ipinfo.io/json')
    #     time.sleep(3)

    proxy = f"148.72.165.7:30127"
    options = uc.ChromeOptions()
    options.add_argument(f'--proxy-server=https://{proxy}')

    driver = uc.Chrome(use_subprocess=False)
    driver.get('https://free-proxy-list.net/')

    # how to scrapt the list on the website and make it a pd DataFrame?

    time.sleep(3)