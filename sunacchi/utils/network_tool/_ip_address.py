# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/23/24
"""
from typing import Union
import requests


def get_public_ip(timeout=5) -> Union[str, None]:
    """
    Gets the public IP address of the machine using an external service.
    Tries to get the IP from api.ipify.org first, then falls back to ifconfig.me if the first one fails.

    Parameters:
    timeout (int): The maximum amount of time to wait for a response from the server in seconds. Default is 5 seconds.

    Returns:
    Union[str, None]: The public IP address as a string, or None if both services fail.
    """
    tool_name = 'api.ipify.org'
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=timeout)
        msg = f"[*INFO*] - get public ip by {tool_name}"
        print(msg)
        return response.json().get("ip")
    except Exception as e:
        print(f"[*Error*] - occurred using {tool_name}: {e}")

    tool_name = 'ipinfo.io'
    try:
        response = requests.get("https://ipinfo.io/ip", timeout=timeout)
        msg = f"[*INFO*] - get public IP by {tool_name}"
        print(msg)
        return response.text.strip()
    except Exception as e:
        print(f"[*Error*] - occurred using {tool_name}: {e}")

    tool_name = 'ifconfig.me'
    try:
        response = requests.get("https://ifconfig.me/ip", timeout=timeout)
        msg = f"[*INFO*] - get public ip by {tool_name}"
        print(msg)
        return response.text.strip()
    except Exception as e:
        print(f"[*Error*] - occurred using {tool_name}: {e}")

    return None
