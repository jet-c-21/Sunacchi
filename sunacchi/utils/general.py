# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/10/24
"""
import time


def wait_countdown(total_second: int, descr='Count Down', clear_console=True):
    while total_second >= 0:
        minutes, seconds = divmod(total_second, 60)
        msg = f"[INFO] - {descr}, {minutes:02d}:{seconds:02d}"
        if clear_console:
            print(msg, end='\r')
        else:
            print(msg)
        time.sleep(1)
        total_second -= 1

    print('\r')
    print('')
