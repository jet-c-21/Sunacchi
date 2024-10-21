# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 6/18/23
"""
from typing import Any
from rich.console import Console

from sunacchi.utils.console_tool.rich_printer import styles as STYLE


class RichPrinter:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RichPrinter, cls).__new__(cls)
            cls._instance.rich_console = Console()
        return cls._instance

    def __init__(self):
        pass

    def __call__(self, msg: Any, style: str = STYLE.DEFAULT):
        self.print(msg, style)

    def print(self, msg: Any, style: str = STYLE.DEFAULT):
        self.rich_console.print(msg, style=style)
