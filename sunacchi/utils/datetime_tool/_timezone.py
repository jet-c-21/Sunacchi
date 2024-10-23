# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/23/24
"""
import os
import time
import platform


def set_os_timezone(timezone: str):
    if platform.system() in ['Linux', 'Darwin']:  # For Linux and macOS
        os.environ['TZ'] = timezone
        time.tzset()  # Apply timezone change
        msg = f"[*INFO*] - Changed timezone to {timezone}"
        print(msg)

    elif platform.system() == 'Windows':  # For Windows
        # Windows doesn't use `TZ` or `tzset()` in the same way
        # Windows timezone changes are typically system-wide and require system-level commands
        print("[*ERROR*] - Changing timezone programmatically is not supported on Windows.")
    else:
        print(f"[*ERROR*] - Unsupported platform: {platform.system()}")
