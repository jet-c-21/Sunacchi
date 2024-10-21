# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/21/24
"""
import datetime
from types import FrameType
from typing import List, Dict, Union, Any


class ExceptionCatcherInfo:
    def __init__(self,
                 inspect_curr_frame: FrameType,
                 exception: Exception = None,
                 exception_caught_datatime: datetime.datetime = None):
        """
        """
        self.filename = inspect_curr_frame.f_code.co_filename
        self.lineno = inspect_curr_frame.f_lineno
        self.func_name = f"{inspect_curr_frame.f_code.co_name}()"

        self.exception = exception
        self.exception_name = f"{self.exception.__class__.__name__}"

        if exception_caught_datatime is None:
            self.exception_caught_datatime = datetime.datetime.now()
        else:
            self.exception_caught_datatime = exception_caught_datatime

    @property
    def info_str(self) -> str:
        return f"{self.filename} Line:{self.lineno} {self.func_name} <{self.exception}>"

    def __repr__(self):
        s = f"<{self.__class__.__name__}: {self.info_str}>"
        return s

    def __iter__(self):
        for key in self.__dict__:
            yield key, self.__dict__[key]

    def __getitem__(self, item):
        return self.__dict__[item]
