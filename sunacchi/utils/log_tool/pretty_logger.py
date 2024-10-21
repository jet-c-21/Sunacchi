# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 7/13/23
"""
import datetime
import logging
import sys
import pathlib
import traceback
import pymongo
import importlib
from typing import Union, Callable, Any

from .. import var as VAR
from ..var import aibr as AIBR

from ..general import get_free_space_mb, ExceptionCatcherInfo
from ..notify_tool.line.tool import send_low_free_space_line_notify
from ..file_tool.general import chmod_777
from ..edge_tool.aibr import (
    get_device_id,
    get_location_id,
)




class ICHASELogger:
    LOW_FREE_SPACE_THRESH_MB = VAR.LOW_FREE_SPACE_THRESH_MB
    DEVICE_ISSUES_UPLOAD_MODE = False

    def __init__(self,
                 logger: logging.Logger,
                 log_path: Union[pathlib.Path, None],
                 console_handler: logging.StreamHandler,
                 device_id: str = None,
                 location_id: str = None,
                 check_free_space=True,
                 mute_logger=False,
                 noisy_mute_mode=False):
        self.logger = logger
        self.log_path = log_path
        self.console_handler = console_handler
        if self.log_path is not None:
            self.has_log_file = True
        else:
            self.has_log_file = False
        self.name = self.logger.name
        self.log_lv = self.logger.level
        self.log_lv_name = logging.getLevelName(self.log_lv)

        if device_id is None:
            self.device_id = get_device_id()

        if location_id is None:
            self.location_id = get_location_id()

        self.check_free_space = check_free_space

        if mute_logger:
            self.mute_flag = True
        else:
            self.mute_flag = False

        self.noisy_mute_mode = noisy_mute_mode

        msg = f"{self} created, DEVICE_ISSUES_UPLOAD_MODE: {ICHASELogger.DEVICE_ISSUES_UPLOAD_MODE}"
        self.info(msg)
        self.chmod_777_log_file()
        self.info_server = None
        
    def __repr__(self):
        if self.log_path is not None:
            s = f"<{self.__class__.__name__} : {self.name} (LV:{self.log_lv_name}) ({self.log_path})>"
        else:
            s = f"<{self.__class__.__name__} : {self.name} (LV:{self.log_lv_name}) (no log path)>"
        return s

    @classmethod
    def turn_on_device_issues_upload_mode(cls):
        cls.DEVICE_ISSUES_UPLOAD_MODE = True

    @classmethod
    def turn_off_device_issues_upload_mode(cls):
        cls.DEVICE_ISSUES_UPLOAD_MODE = False

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
        self.noisy_mute_mode = True

    def turn_off_noisy_mute(self):
        msg = f"turn off noisy mute mode"
        self.logger.info(msg)
        self.noisy_mute_mode = False

    def chmod_777_log_file(self):
        if self.has_log_file and self.log_path.is_file():
            self.log_path.chmod(0o777)
            self.log_path.parent.chmod(0o777)

    def __evoke_log_func(self, msg: object, log_func: Callable):
        # if not self.log_path.is_file():
        #     try:
        #         self.log_path.touch()
        #         self.log_path.chmod(0o777)
        #     except:
        #         pass

        try:
            log_func(msg)
        except Exception as e:
            msg = f"[*WARN*] - [{self.__class__.__name__}] - [Log Func Evoke Error] - " \
                  f"failed to evoke {log_func.__name__}() with msg: {msg}, Error: {e}"
            print(msg)

    def __do_log(self, msg: object, log_func: Callable):
        self.update_console_handler_log_lv()
        if self.has_log_file:
            if self.check_free_space:
                curr_free_space_mb = get_free_space_mb()
                if curr_free_space_mb > self.LOW_FREE_SPACE_THRESH_MB:
                    self.__evoke_log_func(msg, log_func)
                else:
                    print(f"[{log_func.__name__}] : {msg}")
                    send_low_free_space_line_notify()
                    raise RuntimeError('Low Free Space Danger Error')
            else:
                self.__evoke_log_func(msg, log_func)
        else:
            self.__evoke_log_func(msg, log_func)

    def debug(self, msg: object, *args, **kwargs):
        if not self.mute_flag:
            self.__do_log(msg, self.logger.debug)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [DEBUG] - {msg}")

    def info(self, msg: object, *args, **kwargs):
        if not self.mute_flag:
            self.__do_log(msg, self.logger.info)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [INFO] - {msg}")

    def warning(self, msg: Any, *args, **kwargs):
        if not self.mute_flag:
            self.__do_log(msg, self.logger.warning)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [WARNING] - {msg}")

        if ICHASELogger.DEVICE_ISSUES_UPLOAD_MODE:
            self.upload_device_issue(self.name, 'warning', msg)

    def error(self, msg: Any, *args, **kwargs):
        if not self.mute_flag:
            self.__do_log(msg, self.logger.error)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [ERROR] - {msg}")

        if ICHASELogger.DEVICE_ISSUES_UPLOAD_MODE:
            self.upload_device_issue(self.name, 'error', msg)

    def critical(self, msg: object, *args, **kwargs):
        if not self.mute_flag:
            self.__do_log(msg, self.logger.critical)
        else:
            if self.noisy_mute_mode:
                print(f"[NOISY MUTE MODE] - [CRITICAL] - {msg}")

        if ICHASELogger.DEVICE_ISSUES_UPLOAD_MODE:
            self.upload_device_issue(self.name, 'critical', msg)

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

        self.__do_log(msg, self.logger.exception)

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

    def upload_device_issue(self, logger_name: str = None, issue_level: str = None, issue: Union[str, Any] = None):
        if self.device_id is None:
            msg = f"[*INFO*] - [{self.name}] - device_id is None, cannot upload device issue"
            print(msg)
            return
        if logger_name is None:
            logger_name = self.name

        try:
            if self.info_server is None:
                from ..api.info_server import InfoServer
                self.info_server = InfoServer()
                
            if self.info_server.can_upload("DEVICE_ISSUES",self.device_id):
                self.turn_on_device_issues_upload_mode()
            else:
                self.turn_off_device_issues_upload_mode()
            
            if isinstance(issue, Exception):
                issue = f"{issue}"
            db_var_cls = AIBR.DB.MG.DEVICE_ISSUES
            db_name = db_var_cls.DB_NAME
            data_datetime = datetime.datetime.now()
            doc = {
                db_var_cls.Field.location_id: self.location_id,
                db_var_cls.Field.logger_name: logger_name,
                db_var_cls.Field.issue_level: issue_level,
                db_var_cls.Field.issue: issue,
                db_var_cls.Field.data_datetime: data_datetime,
                db_var_cls.Field.created_datetime: data_datetime,
                db_var_cls.Field.updated_datetime: data_datetime
            }

            status, response =self.info_server.insert_one(db_name, self.device_id, doc)
            if status:
                return response
            else:
                msg = f"[*WARN*] - [{self.name}] - cannot upload device issue, Error: {e}"
                print(msg)
                raise

        except Exception as e:
            msg = f"[*WARN*] - [{self.name}] - cannot upload device issue, Error: {e}"
            print(msg)
