# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/21/24
"""
from typing import Union
import pathlib
import logging

from sunacchi.utils.hash_tool import get_obj_mem_md5_id
from sunacchi.utils.log_tool.pretty_logger import PrettyLogger
from sunacchi.utils.log_tool.logger_factory import create_logger


def get_cls_instance_logger_name(cls_instance: object, length=6, upper=True) -> str:
    cls_emoji = getattr(cls_instance, 'CLS_EMOJI', None)
    if cls_emoji is not None:
        logger_name = f"{cls_emoji} {cls_instance.__class__.__name__}-{get_obj_mem_md5_id(cls_instance, length, upper=upper)}"
    else:
        logger_name = f"{cls_instance.__class__.__name__}-{get_obj_mem_md5_id(cls_instance, length, upper=upper)}"

    return logger_name


def get_cls_instance_logger(
        cls_instance: object,
        log_lv=logging.DEBUG,
        log_path: Union[pathlib.Path, str, None] = 'default',
        logger_prefix=None,
        logger_suffix=None,
        logger_id_len=6,
        logger_id_upper=True,
        mute_logger=False,
        max_save_mb=5,
        backup_count=0) -> PrettyLogger:
    logger_name = get_cls_instance_logger_name(
        cls_instance,
        length=logger_id_len,
        upper=logger_id_upper
    )

    if logger_prefix is not None:
        logger_name = f"{logger_prefix}{logger_name}"

    if logger_suffix is not None:
        logger_name = f"{logger_name}{logger_suffix}"

    logger = create_logger(
        logger_name,
        log_lv=log_lv,
        log_path=log_path,
        mute_logger=mute_logger,
        max_save_mb=max_save_mb,
        backup_count=backup_count
    )

    return logger
