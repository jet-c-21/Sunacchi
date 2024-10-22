# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/22/24
"""
import sys
import os
import platform
import subprocess

# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/22/24
"""
import sys
import os
import platform
import subprocess
from sunacchi.utils.log_tool import PrettyLogger
from sunacchi.utils.system_tool import get_curr_process_work_root_dir


def launch_maxbot_main_script_in_subprocess(script_name='chrome_tixcraft',
                                            filename='',
                                            homepage='',
                                            kktix_account='',
                                            kktix_password='',
                                            window_size='',
                                            headless='false',
                                            logger: PrettyLogger = None):
    _cmd_argument_ls = list()
    if filename:
        _cmd_argument_ls.append(f'--input={filename}')
    if homepage:
        _cmd_argument_ls.append(f'--homepage={homepage}')
    if kktix_account:
        _cmd_argument_ls.append(f'--kktix_account={kktix_account}')
    if kktix_password:
        _cmd_argument_ls.append(f'--kktix_password={kktix_password}')
    if window_size:
        _cmd_argument_ls.append(f'--window_size={window_size}')
    if headless:
        _cmd_argument_ls.append(f'--headless={headless}')

    # working_dir = os.path.dirname(os.path.realpath(__file__)) # old version, supposed to be PROJECT_DIR
    working_dir = get_curr_process_work_root_dir()
    if logger is not None:
        msg = f"maxbot launched working_dir: {working_dir}"
        logger.info(msg)

    platform_system = platform.system()

    if hasattr(sys, 'frozen'):
        if logger is not None:
            msg = f"execute in frozen mode"
            logger.info(msg)

        # Set command for frozen mode based on platform
        if platform_system == 'Windows':
            cmd = f"{script_name}.exe " + ' '.join(_cmd_argument_ls)
        else:
            cmd = f"./{script_name} " + ' '.join(_cmd_argument_ls)

        if logger is not None:
            if platform_system == 'Darwin':
                msg = f"execute cmd on MacOS: {cmd}"
                logger.info(msg)

            elif platform_system == 'Linux':
                msg = f"execute cmd on Linux: {cmd}"
                logger.info(msg)

            elif platform_system == 'Windows':
                msg = f"execute cmd on Windows: {cmd}"
                logger.info(msg)

            else:
                msg = f"execute cmd on unknown platform: {cmd}"
                logger.warning(msg)

        subprocess.Popen(cmd, shell=True, cwd=working_dir)

    else:
        if logger is not None:
            msg = f"execute with python interpreter"
            logger.info(msg)

        # Set interpreter based on platform
        interpreter_binary = 'python3' if platform_system != 'Windows' else 'python'
        interpreter_binary_alt = 'python' if platform_system != 'Windows' else 'python3'

        script_path = f"{script_name}.py"

        _arg_ls_of_cmd = [interpreter_binary, script_path] + _cmd_argument_ls
        try:
            if logger is not None:
                msg = f"try to execute {script_path} with interpreter: {interpreter_binary}"
                logger.debug(msg)

            subprocess.Popen(_arg_ls_of_cmd, cwd=working_dir)

            if logger is not None:
                msg = f"successfully executed {script_path} with interpreter: {interpreter_binary}"
                logger.info(msg)

            return
        except Exception as e:
            if logger is not None:
                msg = f"failed to execute {script_path} with interpreter: {interpreter_binary}, Error: {e}"
                logger.exception(msg)

        _arg_ls_of_cmd = [interpreter_binary_alt, script_path] + _cmd_argument_ls
        try:
            if logger is not None:
                msg = f"try to execute {script_path} with alternate interpreter: {interpreter_binary_alt}"
                logger.debug(msg)

            subprocess.Popen(_arg_ls_of_cmd, cwd=working_dir)

            if logger is not None:
                msg = f"successfully executed {script_path} with alternate interpreter: {interpreter_binary_alt}"
                logger.info(msg)

            return
        except Exception as e:
            if logger is not None:
                msg = f"failed to execute {script_path} with interpreter: {interpreter_binary_alt}, Error: {e}"
                logger.exception(msg)
