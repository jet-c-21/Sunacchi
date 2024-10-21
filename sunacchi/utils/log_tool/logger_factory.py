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

from sunacchi.utils.file_tool import create_dir
from sunacchi.utils.log_tool.pretty_logger import PrettyLogger
from sunacchi.utils.console_tool.rich_printer import RichPrinter
from sunacchi.utils.system_tool import get_curr_process_work_root_dir


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
    def __init__(self, log_file: pathlib.Path):
        log_file = pathlib.Path(log_file)
        if log_file.parent.name != '' and not log_file.parent.is_dir():
            create_dir(log_file.parent)
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
                  mute_logger=False,
                  max_save_mb=5,
                  backup_count=0,
                  verbose=False) -> PrettyLogger:
    if name in LOGGER_DICT:
        return LOGGER_DICT[name]

    if verbose:
        rich_printer = RichPrinter()
    else:
        rich_printer = None

    logger = logging.getLogger(name)
    logger.setLevel(log_lv)

    msg = f"new logger name: {logger.name}, LEVEL: {logging.getLevelName(logger.level)} ({logger.level})"
    if not mute_logger:
        if verbose:
            rich_printer(msg)

    console_handler.setLevel(log_lv)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_path is not None:
        # # >>> check disk free space >>>
        # curr_free_space_mb = get_free_space_mb()
        # if check_free_space:
        #     if curr_free_space_mb < VAR.LOW_FREE_SPACE_THRESH_MB:
        #         msg = f"[WARNING] - Device is at Low Free Space: {get_free_space_mb(to_int=True)}"
        #         rich_printer(msg)
        #         raise VAR.LOW_FREE_SPACE_ERROR
        # # <<< check disk free space <<<

        if log_path == 'default':
            _log_file_dest_path = get_curr_process_work_root_dir() / 'logs' / 'sunacchi-dflt.log'

        else:
            _log_file_dest_path = pathlib.Path(log_path)

        if backup_count == 0:
            file_handler = FileHandler(_log_file_dest_path)
        else:
            # Auto-refresh is allowed only if the backup count exceeds 1.
            file_handler = CustomRotatingFileHandler(_log_file_dest_path, max_mb=max_save_mb, backup_count=backup_count)

        file_handler_formatter = logging.Formatter(
            '⏰ %(asctime)s <%(name)s> [%(levelname)s] 📝 %(message)s'
        )
        file_handler.setFormatter(file_handler_formatter)
        file_handler.setLevel(log_lv)
        logger.addHandler(file_handler)

        msg = f"<{name}>'s log file = {file_handler.baseFilename}"
        if not mute_logger:
            if verbose:
                rich_printer(msg)

        log_path = pathlib.Path(file_handler.baseFilename)
        try:
            log_path.parent.chmod(0o777)
        except Exception as e:
            print(f"[logger_factory] [create_logger()] - failed to chmod log file parent folder to 0o777, Error: {e}")

        new_logger = PrettyLogger(
            logger,
            log_path,
            console_handler,
            mute_logger=mute_logger,
        )
        try:
            log_path.chmod(0o777)
        except Exception as e:
            print(f"[logger_factory] [create_logger()] - failed to chmod log file to 0o777, Error: {e}")

    else:
        new_logger = PrettyLogger(
            logger,
            None,
            console_handler,
        )

    LOGGER_DICT[new_logger.name] = new_logger

    return new_logger
