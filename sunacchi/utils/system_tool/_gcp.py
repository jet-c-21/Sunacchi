# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/23/24
"""
import requests


def curr_machine_is_gcp_vm() -> bool:
    try:
        # GCP metadata server is available at this URL
        response = requests.get(
            "http://metadata.google.internal/computeMetadata/v1/instance/",
            headers={"Metadata-Flavor": "Google"},
            timeout=2  # Set a short timeout for quick response
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
