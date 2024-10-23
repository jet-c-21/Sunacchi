# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/21/24
"""
import pathlib
import sys

# add project directory to path
curr_file_path = pathlib.Path(__file__).absolute()
CURR_DIR = curr_file_path.parent
PROJECT_DIR = CURR_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

from sunacchi.utils.log_tool import (
    create_logger,
    get_cls_instance_logger
)

if __name__ == '__main__':
    logger = create_logger('has-log-file-logger', log_path='has-log-file-logger.log')
    logger.info('check log file')

    no_log_file_logger = create_logger('no-log-file-logger', log_path=None)
    logger.debug('i should not create any log file')
    logger.info('i should not create any log file')
    logger.warning('i should not create any log file')
    logger.error('i should not create any log file')
    logger.critical('i should not create any log file')
