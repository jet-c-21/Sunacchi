# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/20/24
"""
import pathlib

import pandas as pd
from bs4 import BeautifulSoup
import requests

from sunacchi.utils.file_tool import create_dir


def get_free_proxy_server_df_from_free_proxy_list_dot_net(
        url='https://free-proxy-list.net/') -> pd.DataFrame:
    # Get the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table
    table = soup.find('div', class_='fpl-list').find('table')

    # Extract the headers
    headers = [header.text for header in table.find_all('th')]

    # Extract the rows
    rows = list()
    for row in table.find_all('tr')[1:]:  # Skip the header row
        rows.append([cell.text for cell in row.find_all('td')])

    # Create a DataFrame
    df = pd.DataFrame(rows, columns=headers)

    return df


def create_free_proxy_server_csv_from_free_proxy_list_dot_net(
        output_csv_path: pathlib.Path,
        url='https://free-proxy-list.net/') -> pathlib.Path:
    output_csv_path = pathlib.Path(output_csv_path)
    if not output_csv_path.parent.is_dir():
        create_dir(output_csv_path.parent)

    df = get_free_proxy_server_df_from_free_proxy_list_dot_net(url)
    df.to_csv(output_csv_path, index=False)

    return output_csv_path
