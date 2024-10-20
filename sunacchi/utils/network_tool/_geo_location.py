# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/20/24
"""
from typing import Union, Dict
import socket

import requests


def get_website_server_geo_location(website_url: str,
                                    search_with_domain_ip=False) -> Union[Dict, None]:
    """
    """
    # Remove "https://" or "http://" if present in the URL
    if website_url.startswith("http://") or website_url.startswith("https://"):
        domain = website_url.split("://")[1].replace('/', '')

    else:
        domain = website_url

    try:
        msg = f"[*DEBUG*] - website_url for query: {website_url}, domain: {domain}"
        print(msg)

        # Get the IP address of the website
        if search_with_domain_ip:
            domain = socket.gethostbyname(domain)

        # Use a public API to get the geolocation information based on the IP address
        _query_url = f"http://ip-api.com/json/{domain}"
        msg = f"[*DEBUG*] - query URL: {_query_url}"
        print(msg)

        response = requests.get(_query_url)
        location_data = response.json()

        location_data['website_url'] = website_url

        # Extract relevant location information
        if response.status_code == 200:
            return location_data

        else:
            print(f"[*INFO*] - Failed to retrieve location for domain: {domain}")
            return

    except socket.gaierror:
        print("[*WARN*] - failed to get site's geo info due to invalid website URL or unable to resolve IP address.")

    except Exception as e:
        print(f"[*ERROR*] - failed to get site's geo info, Error: {e}")


