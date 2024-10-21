# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 3/10/23
"""
import logging
import logging.handlers
import os
import pathlib
from typing import Union

from . import DFLT_LOG_PATH
from .. import var as VAR

from .ichase_logger import ICHASELogger
from ..console_tool.rich_printer.rich_printer import RichPrinter
from ..general import get_free_space_mb
from ..notify_tool.line.tool import send_low_free_space_line_notify
from ..edge_tool.aibr import get_device_id


class CustomFormatter(logging.Formatter):
    __LEVEL_COLORS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]
    __FORMATS = None

    @classmethod
    def get_formats(cls):
        if cls.__FORMATS is None:
            cls.__FORMATS = {
                level: logging.Formatter(
                    f'%(asctime)s {color}%(levelname)-3s\x1b[0m \x1b[35m%(name)s\x1b[0m 📝 %(message)s',
                    '%Y-%m-%d %H:%M:%S'
                )
                for level, color in cls.__LEVEL_COLORS
            }
        return cls.__FORMATS

    def format(self, record):
        formatter = self.get_formats().get(record.levelno)
        if formatter is None:
            formatter = self.get_formats()[logging.DEBUG]

        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)
        record.exc_text = None
        return output


class FileHandler(logging.FileHandler):
    def __init__(self, log_file):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        super().__init__(log_file, encoding='utf-8')

class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, log_file, max_mb=5, backup_count=1):        
        os.makedirs(os.path.dirname(log_file), exist_ok=True)        
        super().__init__(log_file, 
                         maxBytes=max_mb * 1024 * 1024,  # X MB
                         backupCount=backup_count,  
                         encoding='utf-8')

class ConsoleHandler(logging.StreamHandler):
    pass


formatter = CustomFormatter()
console_handler = ConsoleHandler()

LOGGER_DICT = dict()


def create_logger(name,
                  log_lv=logging.DEBUG,
                  log_path: Union[pathlib.Path, str, None] = 'default',
                  check_free_space=True,
                  mute_logger=False,
                  max_save_mb=5,
                  backup_count=0) -> ICHASELogger:
    if name in LOGGER_DICT:
        return LOGGER_DICT[name]

    rich_printer = RichPrinter()

    logger = logging.getLogger(name)
    logger.setLevel(log_lv)

    msg = f"new logger name: {logger.name}, LEVEL: {logging.getLevelName(logger.level)} ({logger.level})"
    if not mute_logger:
        rich_printer(msg)

    console_handler.setLevel(log_lv)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_path is not None:
        curr_free_space_mb = get_free_space_mb()
        if check_free_space:
            if curr_free_space_mb < VAR.LOW_FREE_SPACE_THRESH_MB:
                msg = f"[WARNING] - Device is at Low Free Space: {get_free_space_mb(to_int=True)}"
                rich_printer(msg)
                send_low_free_space_line_notify()
                raise VAR.LOW_FREE_SPACE_ERROR
        setting_log_path = ""
        if log_path == 'default':
            setting_log_path = DFLT_LOG_PATH
        else:
            setting_log_path = log_path

        if backup_count == 0:
            file_handler = FileHandler(setting_log_path)
        else:
            # Auto-refresh is allowed only if the backup count exceeds 1.
            file_handler = CustomRotatingFileHandler(setting_log_path, max_mb=max_save_mb, backup_count=backup_count)

        file_handler_formatter = logging.Formatter(
            '⏰ %(asctime)s <%(name)s> [%(levelname)s] 📝 %(message)s'
        )
        file_handler.setFormatter(file_handler_formatter)
        file_handler.setLevel(log_lv)
        logger.addHandler(file_handler)
            
        msg = f"<{name}>'s log file = {file_handler.baseFilename}"
        if not mute_logger:
            rich_printer(msg)

        log_path = pathlib.Path(file_handler.baseFilename)
        try:
            log_path.parent.chmod(0o777)
        except Exception as e :
            print(f"[logger_factory] [create_logger()] :{e}")

        new_logger = ICHASELogger(
            logger,
            log_path,
            console_handler,
            check_free_space=check_free_space,
            mute_logger=mute_logger,
        )
        try:
            log_path.chmod(0o777)
        except Exception as e :
            print(f"[logger_factory] [create_logger()] :{e}")

    else:
        new_logger = ICHASELogger(
            logger,
            None,
            console_handler,
            check_free_space=check_free_space
        )

    LOGGER_DICT[new_logger.name] = new_logger

    return new_logger
