# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/20/24
"""
import datetime


def get_curr_datetime() -> datetime.datetime:
    return datetime.datetime.now()


def get_curr_datetime_str() -> str:
    return get_curr_datetime().strftime('%Y-%m-%d %H:%M:%S')



