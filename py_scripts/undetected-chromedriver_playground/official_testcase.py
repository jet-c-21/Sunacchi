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

import json
from sunacchi.utils.file_tool import txt_file_to_str_ls
from bs4 import BeautifulSoup
import time
import datetime
from pprint import pprint as pp
import undetected_chromedriver as uc

if __name__ == '__main__':
    free_proxy_ls_txt_file = PROJECT_DIR / 'proxy_servers_files' / 'free-proxy-list.txt'
    # assert free_proxy_ls_txt_file.is_file(), f"File not found: {free_proxy_ls_txt_file}"
    # free_proxy_ls = txt_file_to_str_ls(free_proxy_ls_txt_file)

    # for proxy in free_proxy_ls:
    #     options = uc.ChromeOptions()
    #     options.add_argument(f'--proxy-server=http://{proxy}')
    #
    #     driver = uc.Chrome(options=options, use_subprocess=False)
    #     driver.get('https://ipinfo.io/json')
    #     time.sleep(3)

    proxy = f"47.251.43.115:33333"  # http works
    # proxy = f"165.232.129.150:80"
    options = uc.ChromeOptions()
    options.add_argument(f'--proxy-server=http://{proxy}')

    print(datetime.datetime.now())
    driver = uc.Chrome(use_subprocess=False, options=options)
    print(datetime.datetime.now())

    get_ip_info_url = 'http://ipinfo.io/json'
    driver.get(get_ip_info_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ip_info_dict = json.loads(soup.text)
    print(f"[*INFO*] - html on {get_ip_info_url}:\n{ip_info_dict}")
    msg = f"[*INFO*] - switch ip at {ip_info_dict.get('country')}, " \
          f"{ip_info_dict.get('region')}"
    print(msg)

    tixcraft_url = 'https://tixcraft.com/'
    driver.get(tixcraft_url)

    time.sleep(3)
