# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/10/24
"""
import asyncio
import time
import time
import datetime
import pytz
import os


def wait_countdown(total_second: int, descr='Count Down', clear_console=True):
    while total_second >= 0:
        minutes, seconds = divmod(total_second, 60)
        msg = f"[INFO] - {descr}, {minutes:02d}:{seconds:02d}"
        if clear_console:
            print(msg, end='\r')
        else:
            print(msg)
        time.sleep(1)
        total_second -= 1

    print('\r')
    print('')


async def async_wait_countdown(total_second: int, descr='Count Down', clear_console=True):
    while total_second >= 0:
        minutes, seconds = divmod(total_second, 60)
        msg = f"[INFO] - {descr}, {minutes:02d}:{seconds:02d}"
        if clear_console:
            print(msg, end='\r')
        else:
            print(msg)
        await asyncio.sleep(1)  # Yield control back to the event loop
        total_second -= 1

    print('\r')
    print('')


def wait_until_time(hour: int,
                    minute: int,
                    second: int = 0,
                    milliseconds: int = 0,  # Added support for milliseconds
                    tz: str = 'Asia/Taipei',
                    descr: str = 'Count Down',
                    clear_console: bool = True,
                    final_range_sec: int = 1):
    """
    Wait until the specified time (hour, minute, second, milliseconds) in the given timezone.

    Parameters:
        hour (int): Hour of the target time (0-23).
        minute (int): Minute of the target time (0-59).
        second (int): Second of the target time (0-59).
        milliseconds (int): Milliseconds of the target time (0-999).
        tz (str): Timezone in which the time should be interpreted.
        descr (str): Description to display while waiting.
        clear_console (bool): Whether to clear the console before displaying countdown.
    """
    timezone = pytz.timezone(tz)
    now = datetime.datetime.now(timezone)

    # Set target time with milliseconds
    target_time = now.replace(hour=hour, minute=minute, second=second, microsecond=milliseconds * 1000)

    # If target time is already passed for today, set it for the next day
    if target_time <= now:
        target_time += datetime.timedelta(days=1)

    is_close_to_end = False
    while True:
        now = datetime.datetime.now(timezone)
        remaining_time = (target_time - now).total_seconds()

        if remaining_time <= 0:
            break

        if not is_close_to_end and clear_console:
            os.system('cls' if os.name == 'nt' else 'clear')

        if not is_close_to_end:
            # Calculate remaining hours, minutes, seconds, and milliseconds
            remaining_hours = int(remaining_time // 3600)
            remaining_minutes = int((remaining_time % 3600) // 60)
            remaining_seconds = int(remaining_time % 60)
            remaining_milliseconds = int((remaining_time * 1000) % 1000)
            print(f"[*INFO*] - {descr}: "
                  f"{remaining_hours:02}:{remaining_minutes:02}:{remaining_seconds:02}.{remaining_milliseconds:03} remaining...")

        # Sleep for a reduced time if close to the target
        if remaining_time > final_range_sec:
            time.sleep(0.1)  # Regular sleep but now faster checks (100 ms)
        else:
            if not is_close_to_end:
                print(f"[*INFO*] - {descr}: less than {final_range_sec} seconds remaining...")
                is_close_to_end = True
            time.sleep(0.001)  # Sleep in finer intervals (1 ms) for the last few seconds

    print("[*INFO*] - Time reached! Proceeding...")
