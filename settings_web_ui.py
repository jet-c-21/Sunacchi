#!/usr/bin/env python3
# coding: utf-8
import asyncio
import base64
import json
import os
import pathlib
import platform
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime

import tornado
from tornado.web import Application
from tornado.web import StaticFileHandler

import sunacchi

from sunacchi.utils import (
    system_tool,
    network_tool,
)

import util
from typing import (
    Dict,
    Any,
    Union,
    Optional,
    Awaitable,
    Tuple,
    List,
    Callable,
    Iterable,
    Generator,
    Type,
    TypeVar,
    cast,
    overload,
)

try:
    import ddddocr
except Exception as exc:
    pass

from sunacchi.application import get_application_timezone
from sunacchi.utils.system_tool import get_python_version
from sunacchi.utils.datetime_tool import set_os_timezone
from sunacchi.utils.log_tool import create_logger
from sunacchi.utils.file_tool import (
    create_dir,
    create_file_from_template,
    read_json,
    to_json,
)
from sunacchi.bot import (
    launch_maxbot_main_script_in_subprocess
)

THIS_FILE_PATH = pathlib.Path(__file__).absolute()
THIS_FILE_PARENT_DIR = THIS_FILE_PATH.parent
PROJECT_DIR = THIS_FILE_PARENT_DIR

SETTINGS_TEMPLATES_DIR = PROJECT_DIR / 'settings-templates'
SETTINGS_TPL_FILE = SETTINGS_TEMPLATES_DIR / 'settings.json'

LOG_DIR = PROJECT_DIR / 'logs'
create_dir(LOG_DIR)

# >>> >>> const variables >>> >>>
CONST_APP_VERSION = f"Sunacchi - v{sunacchi.__version__}"

CONST_MAXBOT_ANSWER_ONLINE_FILE = "MAXBOT_ONLINE_ANSWER.txt"
CONST_MAXBOT_CONFIG_FILE = PROJECT_DIR / 'settings.json'
CONST_MAXBOT_EXTENSION_NAME = "Maxbotplus_1.0.0"
CONST_MAXBOT_EXTENSION_STATUS_JSON = "status.json"
CONST_MAXBOT_INT28_FILE = "MAXBOT_INT28_IDLE.txt"
CONST_MAXBOT_LAST_URL_FILE = "MAXBOT_LAST_URL.txt"
CONST_MAXBOT_QUESTION_FILE = "MAXBOT_QUESTION.txt"

CONST_SERVER_PORT = 16888

CONST_FROM_TOP_TO_BOTTOM = "from top to bottom"
CONST_FROM_BOTTOM_TO_TOP = "from bottom to top"
CONST_CENTER = "center"
CONST_RANDOM = "random"
CONST_SELECT_ORDER_DEFAULT = CONST_RANDOM
CONST_EXCLUDE_DEFAULT = "\"輪椅\",\"身障\",\"身心 障礙\",\"Restricted View\",\"燈柱遮蔽\",\"視線不完整\""
CONST_CAPTCHA_SOUND_FILENAME_DEFAULT = "ding-dong.wav"
CONST_HOMEPAGE_DEFAULT = "about:blank"

CONST_OCR_CAPTCH_IMAGE_SOURCE_NON_BROWSER = "NonBrowser"
CONST_OCR_CAPTCH_IMAGE_SOURCE_CANVAS = "canvas"

CONST_WEBDRIVER_TYPE_SELENIUM = "selenium"
CONST_WEBDRIVER_TYPE_UC = "undetected_chromedriver"
CONST_WEBDRIVER_TYPE_DP = "DrissionPage"
CONST_WEBDRIVER_TYPE_NODRIVER = "nodriver"

CONST_SUPPORTED_SITES = [
    "https://kktix.com",
    "https://tixcraft.com (拓元)",
    "https://ticketmaster.sg",
    # "https://ticketmaster.com",
    "https://teamear.tixcraft.com/ (添翼)",
    "https://www.indievox.com/ (獨立音樂)",
    "https://www.famiticket.com.tw (全網)",
    "https://ticket.ibon.com.tw/",
    "https://kham.com.tw/ (寬宏)",
    "https://ticket.com.tw/ (年代)",
    "https://tickets.udnfunlife.com/ (udn售票網)",
    "https://ticketplus.com.tw/ (遠大)",
    "===[香港或南半球的系統]===",
    "http://www.urbtix.hk/ (城市)",
    "https://www.cityline.com/ (買飛)",
    "https://hotshow.hkticketing.com/ (快達票)",
    "https://ticketing.galaxymacau.com/ (澳門銀河)",
    "http://premier.ticketek.com.au"
]

URL_DONATE = 'https://max-everyday.com/about/#donate'
URL_HELP = 'https://max-everyday.com/2018/03/tixcraft-bot/'
URL_RELEASE = 'https://github.com/max32002/tixcraft_bot/releases'
URL_FB = 'https://www.facebook.com/maxbot.ticket'
URL_CHROME_DRIVER = 'https://chromedriver.chromium.org/'
URL_FIREFOX_DRIVER = 'https://github.com/mozilla/geckodriver/releases'
URL_EDGE_DRIVER = 'https://developer.microsoft.com/zh-tw/microsoft-edge/tools/webdriver/'

# <<< <<< const variables <<< <<<
APPLICATION_PYTHON_VERSION = get_python_version()
APPLICATION_TIMEZONE = get_application_timezone(CONST_MAXBOT_CONFIG_FILE)
set_os_timezone(APPLICATION_TIMEZONE)

# global logger
logger_name = f"{THIS_FILE_PATH.stem}"
log_path = LOG_DIR / f"{logger_name}.log"
logger = create_logger(logger_name, log_path=log_path)


def get_default_config() -> Dict:
    """
    TODO:
        seems can get rid of this function in the future

    we have created templates file
    """
    config_dict = dict()

    config_dict["homepage"] = CONST_HOMEPAGE_DEFAULT
    config_dict["browser"] = "chrome"
    config_dict["language"] = "English"
    config_dict["ticket_number"] = 2
    config_dict["refresh_datetime"] = ""

    config_dict["ocr_captcha"] = dict()
    config_dict["ocr_captcha"]["enable"] = True
    config_dict["ocr_captcha"]["beta"] = True
    config_dict["ocr_captcha"]["force_submit"] = True
    config_dict["ocr_captcha"]["image_source"] = CONST_OCR_CAPTCH_IMAGE_SOURCE_CANVAS
    config_dict["webdriver_type"] = CONST_WEBDRIVER_TYPE_UC

    config_dict["date_auto_select"] = dict()
    config_dict["date_auto_select"]["enable"] = True
    config_dict["date_auto_select"]["date_keyword"] = ""
    config_dict["date_auto_select"]["mode"] = CONST_SELECT_ORDER_DEFAULT

    config_dict["area_auto_select"] = dict()
    config_dict["area_auto_select"]["enable"] = True
    config_dict["area_auto_select"]["mode"] = CONST_SELECT_ORDER_DEFAULT
    config_dict["area_auto_select"]["area_keyword"] = ""
    config_dict["keyword_exclude"] = CONST_EXCLUDE_DEFAULT

    config_dict['kktix'] = dict()
    config_dict["kktix"]["auto_press_next_step_button"] = True
    config_dict["kktix"]["auto_fill_ticket_number"] = True
    config_dict["kktix"]["max_dwell_time"] = 60

    config_dict['cityline'] = dict()
    config_dict["cityline"]["cityline_queue_retry"] = True

    config_dict['tixcraft'] = dict()
    config_dict["tixcraft"]["pass_date_is_sold_out"] = True
    config_dict["tixcraft"]["auto_reload_coming_soon_page"] = True

    config_dict['advanced'] = dict()

    config_dict['advanced']['play_sound'] = dict()
    config_dict["advanced"]["play_sound"]["ticket"] = True
    config_dict["advanced"]["play_sound"]["order"] = True
    config_dict["advanced"]["play_sound"]["filename"] = CONST_CAPTCHA_SOUND_FILENAME_DEFAULT

    config_dict["advanced"]["tixcraft_sid"] = ""
    config_dict["advanced"]["ibonqware"] = ""
    config_dict["advanced"]["facebook_account"] = ""
    config_dict["advanced"]["kktix_account"] = ""
    config_dict["advanced"]["fami_account"] = ""
    config_dict["advanced"]["cityline_account"] = ""
    config_dict["advanced"]["urbtix_account"] = ""
    config_dict["advanced"]["hkticketing_account"] = ""
    config_dict["advanced"]["kham_account"] = ""
    config_dict["advanced"]["ticket_account"] = ""
    config_dict["advanced"]["udn_account"] = ""
    config_dict["advanced"]["ticketplus_account"] = ""

    config_dict["advanced"]["facebook_password"] = ""
    config_dict["advanced"]["kktix_password"] = ""
    config_dict["advanced"]["fami_password"] = ""
    config_dict["advanced"]["urbtix_password"] = ""
    config_dict["advanced"]["cityline_password"] = ""
    config_dict["advanced"]["hkticketing_password"] = ""
    config_dict["advanced"]["kham_password"] = ""
    config_dict["advanced"]["ticket_password"] = ""
    config_dict["advanced"]["udn_password"] = ""
    config_dict["advanced"]["ticketplus_password"] = ""

    config_dict["advanced"]["facebook_password_plaintext"] = ""
    config_dict["advanced"]["kktix_password_plaintext"] = ""
    config_dict["advanced"]["fami_password_plaintext"] = ""
    config_dict["advanced"]["urbtix_password_plaintext"] = ""
    config_dict["advanced"]["cityline_password_plaintext"] = ""
    config_dict["advanced"]["hkticketing_password_plaintext"] = ""
    config_dict["advanced"]["kham_password_plaintext"] = ""
    config_dict["advanced"]["ticket_password_plaintext"] = ""
    config_dict["advanced"]["udn_password_plaintext"] = ""
    config_dict["advanced"]["ticketplus_password_plaintext"] = ""

    config_dict["advanced"]["chrome_extension"] = True
    config_dict["advanced"]["disable_adjacent_seat"] = False
    config_dict["advanced"]["hide_some_image"] = False
    config_dict["advanced"]["block_facebook_network"] = False

    config_dict["advanced"]["headless"] = False
    config_dict["advanced"]["verbose"] = False
    config_dict["advanced"]["auto_guess_options"] = True
    config_dict["advanced"]["user_guess_string"] = ""

    # remote_url not under ocr, due to not only support ocr features.
    config_dict["advanced"]["remote_url"] = f"http://127.0.0.1:{CONST_SERVER_PORT}/"

    config_dict["advanced"]["auto_reload_page_interval"] = 0.1
    config_dict["advanced"]["auto_reload_overheat_count"] = 4
    config_dict["advanced"]["auto_reload_overheat_cd"] = 1.0
    config_dict["advanced"]["reset_browser_interval"] = 0
    config_dict["advanced"]["proxy_server_port"] = ""
    config_dict["advanced"]["window_size"] = "480,1024"

    config_dict["advanced"]["idle_keyword"] = ""
    config_dict["advanced"]["resume_keyword"] = ""
    config_dict["advanced"]["idle_keyword_second"] = ""
    config_dict["advanced"]["resume_keyword_second"] = ""

    return config_dict


def read_last_url_from_file() -> str:
    text = ""
    if os.path.exists(CONST_MAXBOT_LAST_URL_FILE):
        try:
            with open(CONST_MAXBOT_LAST_URL_FILE, "r") as text_file:
                text = text_file.readline()
        except Exception as e:
            pass

    return text


def _load_settings_from_local_json_file(do_log=True) -> Tuple[pathlib.Path, Dict]:
    """
    load config dict from settings.json
    if the json is not existed it will create a new one from template
    """
    _config_json_file = CONST_MAXBOT_CONFIG_FILE

    if do_log:
        msg = f"config json file to load: {_config_json_file}"
        logger.debug(msg)

    if not _config_json_file.is_file():
        _config_json_file = create_file_from_template(
            _config_json_file, SETTINGS_TPL_FILE
        )
        msg = f"config json file is not existed,\n" \
              f"created from template: {SETTINGS_TPL_FILE},\n" \
              f"new config json file: {_config_json_file}"
        logger.debug(msg)

    _config_dict = read_json(_config_json_file)
    if _config_dict is None:
        _config_dict = get_default_config()
        msg = f"failed to read config json content from local file, get default config instead"
        logger.warning(msg)

    if do_log:
        msg = f"loaded config dict key count: {len(_config_dict)}, json file path: {_config_json_file}"
        logger.debug(msg)

    return _config_json_file, _config_dict


def _reset_local_settings_json_file() -> Tuple[pathlib.Path, Dict]:
    msg = f"start doing _reset_local_settings_json_file() ..."
    logger.debug(msg)

    config_filepath = CONST_MAXBOT_CONFIG_FILE
    if config_filepath.is_file():
        try:
            config_filepath.unlink()
        except Exception as e:
            msg = f"[*WARN*] - failed to deleted config file: {config_filepath}, Error: {e}"
            print(msg)

    msg = f"finish doing _reset_local_settings_json_file()"
    logger.debug(msg)

    return _load_settings_from_local_json_file()


def decrypt_password(config_dict):
    config_dict["advanced"]["facebook_password"] = util.decryptMe(config_dict["advanced"]["facebook_password"])
    config_dict["advanced"]["kktix_password"] = util.decryptMe(config_dict["advanced"]["kktix_password"])
    config_dict["advanced"]["fami_password"] = util.decryptMe(config_dict["advanced"]["fami_password"])
    config_dict["advanced"]["cityline_password"] = util.decryptMe(config_dict["advanced"]["cityline_password"])
    config_dict["advanced"]["urbtix_password"] = util.decryptMe(config_dict["advanced"]["urbtix_password"])
    config_dict["advanced"]["hkticketing_password"] = util.decryptMe(config_dict["advanced"]["hkticketing_password"])
    config_dict["advanced"]["kham_password"] = util.decryptMe(config_dict["advanced"]["kham_password"])
    config_dict["advanced"]["ticket_password"] = util.decryptMe(config_dict["advanced"]["ticket_password"])
    config_dict["advanced"]["udn_password"] = util.decryptMe(config_dict["advanced"]["udn_password"])
    config_dict["advanced"]["ticketplus_password"] = util.decryptMe(config_dict["advanced"]["ticketplus_password"])
    return config_dict


def encrypt_password(config_dict):
    config_dict["advanced"]["facebook_password"] = util.encryptMe(config_dict["advanced"]["facebook_password"])
    config_dict["advanced"]["kktix_password"] = util.encryptMe(config_dict["advanced"]["kktix_password"])
    config_dict["advanced"]["fami_password"] = util.encryptMe(config_dict["advanced"]["fami_password"])
    config_dict["advanced"]["cityline_password"] = util.encryptMe(config_dict["advanced"]["cityline_password"])
    config_dict["advanced"]["urbtix_password"] = util.encryptMe(config_dict["advanced"]["urbtix_password"])
    config_dict["advanced"]["hkticketing_password"] = util.encryptMe(config_dict["advanced"]["hkticketing_password"])
    config_dict["advanced"]["kham_password"] = util.encryptMe(config_dict["advanced"]["kham_password"])
    config_dict["advanced"]["ticket_password"] = util.encryptMe(config_dict["advanced"]["ticket_password"])
    config_dict["advanced"]["udn_password"] = util.encryptMe(config_dict["advanced"]["udn_password"])
    config_dict["advanced"]["ticketplus_password"] = util.encryptMe(config_dict["advanced"]["ticketplus_password"])
    return config_dict


def maxbot_idle():
    app_root = system_tool.get_curr_process_work_root_dir()
    idle_filepath = os.path.join(app_root, CONST_MAXBOT_INT28_FILE)
    try:
        with open(CONST_MAXBOT_INT28_FILE, "w") as text_file:
            text_file.write("")
    except Exception as e:
        pass


def maxbot_resume():
    app_root = system_tool.get_curr_process_work_root_dir()
    idle_filepath = os.path.join(app_root, CONST_MAXBOT_INT28_FILE)
    for i in range(3):
        util.force_remove_file(idle_filepath)


def launch_maxbot():
    """
    1. decide which script to launch
    2. do window size handling
    3. start the script with another Thread

    """
    msg = f"start doing launch_maxbot() ..."
    logger.info(msg)

    global bot_launched_count
    # if "launch_counter" in globals():
    #     bot_launched_count += 1
    # else:
    #     bot_launched_count = 0

    bot_launched_count += 1

    config_filepath, config_dict = _load_settings_from_local_json_file()
    config_dict = decrypt_password(config_dict)

    script_name = 'chrome_tixcraft'
    if config_dict['webdriver_type'] == CONST_WEBDRIVER_TYPE_NODRIVER:
        script_name = 'nodriver_tixcraft'

    # do window size handling
    window_size = config_dict['advanced']['window_size']
    if len(window_size) > 0:
        if ',' in window_size:
            size_array = window_size.split(',')
            target_width = int(size_array[0])
            target_left = target_width * bot_launched_count
            # print("target_left:", target_left)
            if target_left >= 1440:
                bot_launched_count = 0
            window_size = window_size + ',' + str(bot_launched_count)
            # print("window_size:", window_size)

    threading.Thread(
        target=launch_maxbot_main_script_in_subprocess,
        name='bot-main-script-launcher-thread',
        kwargs={
            'script_name': script_name,
            'filename': '',
            'homepage': '',
            'kktix_account': '',
            'kktix_password': '',
            'window_size': window_size,
            'headless': '',
            'logger': logger
        },
    ).start()

    msg = f"start bot-main-script-launcher-thread with script_name: {script_name}, window_size: {window_size}"
    logger.info(msg)

    msg = f"finish doing launch_maxbot()\n"
    logger.info(msg)


def clean_extension_status():
    Root_Dir = system_tool.get_curr_process_work_root_dir()
    webdriver_path = os.path.join(Root_Dir, "webdriver")
    target_path = os.path.join(webdriver_path, CONST_MAXBOT_EXTENSION_NAME)
    target_path = os.path.join(target_path, "data")
    target_path = os.path.join(target_path, CONST_MAXBOT_EXTENSION_STATUS_JSON)
    if os.path.exists(target_path):
        try:
            os.unlink(target_path)
        except Exception as exc:
            print(exc)
            pass


def sync_status_to_extension(status):
    Root_Dir = system_tool.get_curr_process_work_root_dir()
    webdriver_path = os.path.join(Root_Dir, "webdriver")
    target_path = os.path.join(webdriver_path, CONST_MAXBOT_EXTENSION_NAME)
    target_path = os.path.join(target_path, "data")
    if os.path.exists(target_path):
        target_path = os.path.join(target_path, CONST_MAXBOT_EXTENSION_STATUS_JSON)
        # print("save as to:", target_path)
        status_json = {}
        status_json["status"] = status
        # print("dump json to path:", target_path)
        try:
            with open(target_path, 'w') as outfile:
                json.dump(status_json, outfile)
        except Exception as e:
            pass


def clean_tmp_file():
    remove_file_list = [
        CONST_MAXBOT_LAST_URL_FILE,
        CONST_MAXBOT_INT28_FILE,
        CONST_MAXBOT_ANSWER_ONLINE_FILE,
        CONST_MAXBOT_QUESTION_FILE
    ]
    for filepath in remove_file_list:
        util.force_remove_file(filepath)


class QuestionHandler(tornado.web.RequestHandler):
    def get(self):
        global txt_question
        txt_question.insert("1.0", "")


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"version": self.application.version})


class ShutdownHandler(tornado.web.RequestHandler):
    def get(self):
        global GLOBAL_SERVER_SHUTDOWN
        GLOBAL_SERVER_SHUTDOWN = True
        self.write({"showdown": GLOBAL_SERVER_SHUTDOWN})


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        is_paused = False
        if os.path.exists(CONST_MAXBOT_INT28_FILE):
            is_paused = True
        url = read_last_url_from_file()
        self.write({"status": not is_paused, "last_url": url})


class PauseHandler(tornado.web.RequestHandler):
    def get(self):
        maxbot_idle()
        self.write({"pause": True})


class ResumeHandler(tornado.web.RequestHandler):
    def get(self):
        maxbot_resume()
        self.write({"resume": True})


class RunHandler(tornado.web.RequestHandler):
    def get(self):
        msg = f"received GET request from RunHandler"
        logger.info(msg)

        launch_maxbot()
        self.write({"run": True})


class LoadJsonHandler(tornado.web.RequestHandler):
    def get(self):
        msg = f"received GET request from LoadJsonHandler"
        logger.debug(msg)

        config_filepath, config_dict = _load_settings_from_local_json_file()
        config_dict = decrypt_password(config_dict)
        self.write(config_dict)


class ResetJsonHandler(tornado.web.RequestHandler):
    def get(self):
        config_filepath, config_dict = _reset_local_settings_json_file()
        util.save_json(config_dict, config_filepath)
        self.write(config_dict)


class SaveJsonHandler(tornado.web.RequestHandler):
    def post(self):
        msg = f"received POST request from SaveJsonHandler"
        logger.debug(msg)

        _body = None
        is_pass_check = True
        error_message = ""
        error_code = 0

        if is_pass_check:
            is_pass_check = False
            try:
                _body = json.loads(self.request.body)
                is_pass_check = True
            except Exception:
                error_message = "wrong json format"
                error_code = 1002
                pass

        if is_pass_check:
            app_root = system_tool.get_curr_process_work_root_dir()
            config_filepath = CONST_MAXBOT_CONFIG_FILE
            config_dict = encrypt_password(_body)

            if config_dict["kktix"]["max_dwell_time"] > 0:
                if config_dict["kktix"]["max_dwell_time"] < 15:
                    # min value is 15 seconds.
                    config_dict["kktix"]["max_dwell_time"] = 15

            if config_dict["advanced"]["reset_browser_interval"] > 0:
                if config_dict["advanced"]["reset_browser_interval"] < 20:
                    # min value is 20 seconds.
                    config_dict["advanced"]["reset_browser_interval"] = 20

            # due to cloudflare.
            if ".cityline.com" in config_dict["homepage"]:
                config_dict["webdriver_type"] = CONST_WEBDRIVER_TYPE_NODRIVER

            to_json(config_dict, config_filepath)

        if not is_pass_check:
            self.set_status(401)
            self.write(dict(error=dict(message=error_message, code=error_code)))

        self.finish()


class OcrHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"answer": "1234"})

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        _body = None
        is_pass_check = True
        errorMessage = ""
        errorCode = 0

        if is_pass_check:
            is_pass_check = False
            try:
                _body = json.loads(self.request.body)
                is_pass_check = True
            except Exception:
                errorMessage = "wrong json format"
                errorCode = 1001
                pass

        img_base64 = None
        image_data = ""
        if is_pass_check:
            if 'image_data' in _body:
                image_data = _body['image_data']
                if len(image_data) > 0:
                    img_base64 = base64.b64decode(image_data)
            else:
                errorMessage = "image_data not exist"
                errorCode = 1002

        # print("is_pass_check:", is_pass_check)
        # print("errorMessage:", errorMessage)
        # print("errorCode:", errorCode)
        ocr_answer = ""
        if not img_base64 is None:
            try:
                ocr_answer = self.application.ocr.classification(img_base64)
                msg = f"predicted ocr_answer: {ocr_answer}"
                logger.info(msg)

            except Exception as e:
                msg = f"failed to get predicted ocr_answer, Error: {e}"
                logger.exception(msg)

        self.write({"answer": ocr_answer})


class QueryHandler(tornado.web.RequestHandler):
    def format_config_keyword_for_json(self, user_input):
        if len(user_input) > 0:
            if not ('\"' in user_input):
                user_input = '"' + user_input + '"'
        return user_input

    def compose_as_json(self, user_input):
        user_input = self.format_config_keyword_for_json(user_input)
        return "{\"data\":[%s]}" % user_input

    def get(self):
        global txt_answer_value
        answer_text = ""
        try:
            answer_text = txt_answer_value.get().strip()
        except Exception as exc:
            pass
        answer_text_output = self.compose_as_json(answer_text)
        # print("answer_text_output:", answer_text_output)
        self.write(answer_text_output)


async def _web_server_main():
    msg = f"start running main_server() ..."
    logger.info(msg)

    ocr = None
    try:
        ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
        msg = f"ddddocr ocr object loaded."
        logger.info(msg)
    except Exception as e:
        msg = f"failed to load ddddocr ocr object, Error: {e}"
        logger.exception(msg)

    app = Application(
        [
            ("/version", VersionHandler),
            ("/shutdown", ShutdownHandler),

            # status api
            ("/status", StatusHandler),
            ("/pause", PauseHandler),
            ("/resume", ResumeHandler),
            ("/run", RunHandler),

            # json api
            ("/load", LoadJsonHandler),
            ("/save", SaveJsonHandler),
            ("/reset", ResetJsonHandler),

            ("/ocr", OcrHandler),
            ("/query", QueryHandler),
            ("/question", QuestionHandler),
            ('/(.*)', StaticFileHandler, {"path": os.path.join(".", 'www/')}),
        ]
    )

    app.ocr = ocr
    app.version = CONST_APP_VERSION

    msg = f"finish setting up api handlers"
    logger.info(msg)

    app.listen(CONST_SERVER_PORT)
    msg = f"server running on port: {CONST_SERVER_PORT}"
    logger.info(msg)

    url = f"http://127.0.0.1:{CONST_SERVER_PORT}/settings.html"

    msg = f"server url: {url}"
    logger.info(msg)

    try:
        webbrowser.open_new(url)
        msg = f"opened homepage with user default browser"
        logger.info(msg)
    except Exception as e:
        msg = f"failed to open homepage with user default browser, Error: {e}"
        logger.exception(msg)

    msg = f"🚀🚀🚀 finish running main_server() 🚀🚀🚀 start waiting for event"
    logger.info(msg)
    await asyncio.Event().wait()


def launch_web_server():
    host = 'localhost'
    port = CONST_SERVER_PORT
    is_port_bound = network_tool.port_is_connectable(
        host=host,
        port=port
    )

    if not is_port_bound:
        asyncio.run(_web_server_main())

    else:
        msg = f"port: {CONST_SERVER_PORT} on host: {host} is already in used"
        logger.warning(msg)
        raise RuntimeError(msg)


def _change_maxbot_status_by_keyword(do_log=False):
    """
    this function will consistently be evoked by status-updating-thread
    """
    if do_log:
        msg = f"start doing change_maxbot_status_by_keyword() ..."
        logger.debug(msg)

    config_filepath, config_dict = _load_settings_from_local_json_file(do_log=False)

    system_clock_data = datetime.now()
    current_time = system_clock_data.strftime('%H:%M:%S')
    # print('Current Time is:', current_time)
    # print("idle_keyword", config_dict["advanced"]["idle_keyword"])
    if len(config_dict["advanced"]["idle_keyword"]) > 0:
        is_matched = util.is_text_match_keyword(config_dict["advanced"]["idle_keyword"], current_time)
        if is_matched:
            # print("match to idle:", current_time)
            maxbot_idle()

    # print("resume_keyword", config_dict["advanced"]["resume_keyword"])
    if len(config_dict["advanced"]["resume_keyword"]) > 0:
        is_matched = util.is_text_match_keyword(config_dict["advanced"]["resume_keyword"], current_time)
        if is_matched:
            # print("match to resume:", current_time)
            maxbot_resume()

    current_time = system_clock_data.strftime('%S')
    if len(config_dict["advanced"]["idle_keyword_second"]) > 0:
        is_matched = util.is_text_match_keyword(config_dict["advanced"]["idle_keyword_second"], current_time)
        if is_matched:
            # print("match to idle:", current_time)
            maxbot_idle()

    if len(config_dict["advanced"]["resume_keyword_second"]) > 0:
        is_matched = util.is_text_match_keyword(config_dict["advanced"]["resume_keyword_second"], current_time)
        if is_matched:
            # print("match to resume:", current_time)
            maxbot_resume()

    if do_log:
        msg = f"finish doing change_maxbot_status_by_keyword()"
        logger.debug(msg)


def settings_gui_timer():
    msg = f"gui timer is started"
    logger.info(msg)
    while True:
        _change_maxbot_status_by_keyword()
        time.sleep(0.4)
        if GLOBAL_SERVER_SHUTDOWN:
            break


if __name__ == "__main__":
    global GLOBAL_SERVER_SHUTDOWN
    GLOBAL_SERVER_SHUTDOWN = False

    bot_launched_count = 0

    msg = f"application python version: {sys.version}"
    logger.info(msg)

    start_thread_in_daemon = True
    threading.Thread(
        target=settings_gui_timer,
        name='status-updating-thread',
        daemon=start_thread_in_daemon).start()
    threading.Thread(target=launch_web_server, daemon=start_thread_in_daemon).start()

    clean_tmp_file()
    clean_extension_status()

    logger.info("to close web server, press Ctrl + C")
    while True:
        time.sleep(0.4)
        if GLOBAL_SERVER_SHUTDOWN:
            break
    logger.info("Bye bye, see you next time")
