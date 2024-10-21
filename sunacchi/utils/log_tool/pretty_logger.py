# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 7/13/23
"""
__version__ = "0.0.1"

from typing import Union, Callable, Any
import logging
import pathlib
import traceback

from sunacchi.utils.file_tool import chmod_777
from sunacchi.utils.log_tool.exception_handle import ExceptionCatcherInfo


class PrettyLogger:
    def __init__(self,
                 logger: logging.Logger,
                 log_path: Union[pathlib.Path, None],
                 console_handler: logging.StreamHandler,
                 mute_logger: bool = False,
                 noisy_mute_mode: bool = False):
        """
        mute_logger: bool
            if True, the logger not do any action

        noisy_mute_mode: bool


        """
        self.logger = logger
        self.log_path = log_path
        if self.log_path is not None:
            self.has_log_file = True
        else:
            self.has_log_file = False

        self.console_handler = console_handler

        self.name = self.logger.name
        self.log_lv = self.logger.level
        self.log_lv_name = logging.getLevelName(self.log_lv)

        if noisy_mute_mode and not mute_logger:
            msg = f"[*WARN*] - when using noisy_mute_mode, mute_logger should also be True"
            print(msg)

        if mute_logger:
            self.mute_flag = True
        else:
            self.mute_flag = False

        self.noisy_mute_mode = noisy_mute_mode

        msg = f"{self} have created"
        self.info(msg)
        self.chmod_777_log_file()

    def __repr__(self):
        if self.log_path is not None:
            s = f"<{self.__class__.__name__} : {self.name} (LV:{self.log_lv_name}) ({self.log_path})>"
        else:
            s = f"<{self.__class__.__name__} : {self.name} (LV:{self.log_lv_name}) (no log path)>"
        return s

    def mute_logger(self):
        self.mute_flag = True
        msg = f"logger: {self.name} muted"
        self.logger.info(msg)

    def unmute_logger(self):
        self.mute_flag = False
        msg = f"logger: {self.name} unmuted"
        self.logger.info(msg)

    def turn_on_noisy_mute_mode(self):
        msg = f"turn on noisy mute mode"
        self.logger.info(msg)

        self.mute_flag = True

        self.noisy_mute_mode = True

    def turn_off_noisy_mute(self):
        msg = f"turn off noisy mute mode"
        self.logger.info(msg)

        self.mute_flag = False

        self.noisy_mute_mode = False

    def chmod_777_log_file(self):
        if self.has_log_file and self.log_path.is_file():
            self.log_path.chmod(0o777)
            self.log_path.parent.chmod(0o777)

    def _evoke_log_func(self, msg: object, log_func: Callable):
        try:
            log_func(msg)
        except Exception as e:
            msg = f"[*WARN*] - [{self.__class__.__name__}] - [Log Func Evoke Error] - " \
                  f"failed to evoke {log_func.__name__}() with msg: {msg}, Error: {e}"
            print(msg)

    def _do_log(self, msg: object, log_func: Callable):
        self._evoke_log_func(msg, log_func)

        # # >>>>>> doing different handle based on log file existence >>>>>>
        # if self.has_log_file:
        #     # >>> doing disk free space check every time when logging if log file is enabled >>>
        #     if self.check_free_space:
        #         curr_free_space_mb = get_free_space_mb()
        #         if curr_free_space_mb > self.LOW_FREE_SPACE_THRESH_MB:
        #             self._evoke_log_func(msg, log_func)
        #         else:
        #             msg = f"[*ERROR*] - Low Disk Free Space Error occurred, " \
        #                   f"when evoked [{log_func.__name__}] with msg: {msg}"
        #             print(msg)
        #             raise RuntimeError('Low Disk Free Space Danger Error')
        #     else:
        #         self._evoke_log_func(msg, log_func)
        #     # <<< doing disk free space check every time when logging if log file is enabled <<<
        #
        # else:
        #     self._evoke_log_func(msg, log_func)
        # # <<<<<< doing different handle based on log file existence <<<<<<

    def debug(self, msg: object, *args, **kwargs):
        if not self.mute_flag:
            self._do_log(msg, self.logger.debug)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [DEBUG] - {msg}")

    def info(self, msg: object, *args, **kwargs):
        if not self.mute_flag:
            self._do_log(msg, self.logger.info)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [INFO] - {msg}")

    def warning(self, msg: Any, *args, **kwargs):
        if not self.mute_flag:
            self._do_log(msg, self.logger.warning)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [WARNING] - {msg}")

    def error(self, msg: Any, *args, **kwargs):
        if not self.mute_flag:
            self._do_log(msg, self.logger.error)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [ERROR] - {msg}")

    def critical(self, msg: object, *args, **kwargs):
        if not self.mute_flag:
            self._do_log(msg, self.logger.critical)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [CRITICAL] - {msg}")

    def exception(self,
                  msg: Union[Exception, Any],
                  *args,
                  exc_info=True,
                  e_catcher_info: ExceptionCatcherInfo = None,
                  evoke_additional_error_log_func=True,
                  error_note: str = None,
                  return_traceback_info_str=False,
                  **kwargs) -> Union[None, str]:
        """
        if input msg is not Exception, it will not log Traceback str
        """
        if isinstance(msg, Exception):
            input_exception = msg
        else:
            input_exception = None

        traceback_info_str = None
        if input_exception is not None:
            traceback_info_str = ''.join(
                traceback.format_exception(None, input_exception, input_exception.__traceback__)
            )

        if e_catcher_info is not None:
            traceback_info_str = f"Exception Catcher: {e_catcher_info.info_str}, Error: {input_exception}\n" \
                                 f"{traceback_info_str}"

        if evoke_additional_error_log_func:
            if traceback_info_str is not None:
                if input_exception is not None:
                    _error_msg = f"Exception Name: {input_exception}, {traceback_info_str}"
                else:
                    _error_msg = traceback_info_str

                if error_note is not None:
                    _error_msg = f"Error Note: {error_note}, {_error_msg}"

                self.error(_error_msg)
            else:
                self.error(msg)

        self._do_log(msg, self.logger.exception)

        if return_traceback_info_str:
            return traceback_info_str

    @property
    def handlers(self):
        return self.logger.handlers

    def set_console_handler_log_lv(self, log_lv):
        self.console_handler.setLevel(log_lv)

    def update_console_handler_log_lv(self):
        self.console_handler.setLevel(self.log_lv)

    def refresh_file_handler(self):
        new_handler_ls = list()
        for h in self.logger.handlers:
            if isinstance(h, logging.FileHandler):
                h.close()
                del h
            else:
                new_handler_ls.append(h)

        self.logger.handlers = new_handler_ls

        # Create new file handler
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(self.log_lv)
        file_formatter = logging.Formatter('⏰ %(asctime)s <%(name)s> [%(levelname)s] 📝 %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        msg = f"logger's file_handler refreshed: {self.log_path}"
        self.info(msg)

        chmod_777(self.log_path)
