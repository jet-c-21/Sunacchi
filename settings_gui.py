#!/usr/bin/env python3
# encoding=utf-8
try:
    import tkinter.font as tkfont
    from tkinter import *
    from tkinter import messagebox, ttk
    from tkinter.filedialog import asksaveasfilename
except Exception as e:
    pass

import pathlib
import asyncio
import base64
import json
import os
import platform
import ssl
import subprocess
import sys
import threading
import time
import warnings
import webbrowser
from datetime import datetime

import pyperclip
import tornado
from tornado.web import Application
from urllib3.exceptions import InsecureRequestWarning

import util

try:
    import ddddocr
except Exception as exc:
    pass

from sunacchi.utils.system_tool import curr_machine_is_gcp_vm

from sunacchi.utils import (
    system_tool,
    network_tool
)

THIS_FILE_PATH = pathlib.Path(__file__).absolute()
THIS_FILE_PARENT_DIR = THIS_FILE_PATH.parent
PROJECT_DIR = THIS_FILE_PARENT_DIR

SETTINGS_TEMPLATES_DIR = PROJECT_DIR / 'settings-templates'
SETTINGS_TPL_FILE = SETTINGS_TEMPLATES_DIR / 'settings.json'

CONST_APP_VERSION = "MaxBot (2024.04.23)"

CONST_MAXBOT_ANSWER_ONLINE_FILE = "MAXBOT_ONLINE_ANSWER.txt"
CONST_MAXBOT_CONFIG_FILE_NAME = "settings.json"
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
CONST_SELECT_OPTIONS_DEFAULT = (CONST_FROM_TOP_TO_BOTTOM, CONST_FROM_BOTTOM_TO_TOP, CONST_CENTER, CONST_RANDOM)
CONST_EXCLUDE_DEFAULT = "\"輪椅\",\"身障\",\"身心 障礙\",\"Restricted View\",\"燈柱遮蔽\",\"視線不完整\""
CONST_CAPTCHA_SOUND_FILENAME_DEFAULT = "ding-dong.wav"
CONST_HOMEPAGE_DEFAULT = "https://tixcraft.com"

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

warnings.simplefilter('ignore', InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

translate = {}

URL_DONATE = 'https://max-everyday.com/about/#donate'
URL_HELP = 'https://max-everyday.com/2018/03/tixcraft-bot/'
URL_RELEASE = 'https://github.com/max32002/tixcraft_bot/releases'
URL_FB = 'https://www.facebook.com/maxbot.ticket'
URL_CHROME_DRIVER = 'https://chromedriver.chromium.org/'
URL_FIREFOX_DRIVER = 'https://github.com/mozilla/geckodriver/releases'
URL_EDGE_DRIVER = 'https://developer.microsoft.com/zh-tw/microsoft-edge/tools/webdriver/'

GLOBAL_SERVER_SHUTDOWN = False


def load_translate():
    translate = dict()
    en_us = dict()
    en_us["homepage"] = 'Homepage'
    en_us["browser"] = 'Browser'
    en_us["language"] = 'Language'
    en_us["ticket_number"] = 'Ticker Number'
    en_us["refresh_datetime"] = 'Refresh at specified time'

    en_us["enable"] = 'Enable'
    en_us["recommand_enable"] = "Recommended to enable"

    en_us["auto_press_next_step_button"] = 'KKTIX Press Next Step Button'
    en_us["auto_fill_ticket_number"] = 'Auto Fill Ticket Number'
    en_us["and"] = 'And with'

    en_us["local_dictionary"] = 'Local Dictionary'
    en_us["remote_url"] = 'Remote URL'
    en_us["server_url"] = 'Server URL'
    en_us["auto_guess_options"] = 'Guess Options in Question'
    en_us["user_guess_string"] = 'Fill Answers in Question'
    en_us["preview"] = 'Preview'
    en_us["question"] = 'Question'
    en_us["answer"] = 'Answer'

    en_us["date_auto_select"] = 'Date Auto Select'
    en_us["date_select_order"] = 'Date select order'
    en_us["date_keyword"] = 'Date Keyword'
    en_us["pass_date_is_sold_out"] = 'Pass date is sold out'
    en_us["auto_reload_coming_soon_page"] = 'Reload coming soon page'
    en_us["auto_reload_page_interval"] = 'Reload page interval(sec.)'
    en_us["max_dwell_time"] = 'KKTIX dwell time(sec.)'
    en_us["cityline_queue_retry"] = 'cityline queue retry'
    en_us["reset_browser_interval"] = 'Reset browser interval(sec.)'
    en_us["proxy_server_port"] = 'Proxy IP:PORT'
    en_us["window_size"] = 'Window size'

    en_us["area_select_order"] = 'Area select order'
    en_us["area_keyword"] = 'Area Keyword'
    en_us["area_auto_select"] = 'Area Auto Select'
    en_us["keyword_exclude"] = 'Keyword Exclude'
    en_us[
        "keyword_usage"] = 'Each keyword need double quotes, separated by comma,\nUse space in keyword as AND logic.\nAppend ,\"\" to match all.'

    en_us["ocr_captcha"] = 'OCR captcha'
    en_us["ocr_captcha_ddddocr_beta"] = 'ddddocr beta'
    en_us["ocr_captcha_force_submit"] = 'Away from keyboard'
    en_us["ocr_captcha_image_source"] = 'OCR image source'
    en_us["webdriver_type"] = 'WebDriver type'
    en_us["headless"] = 'Headless mode'
    # Make the operation more talkative
    en_us["verbose"] = 'Verbose mode'
    en_us["running_status"] = 'Running Status'
    en_us["running_url"] = 'Running URL'
    en_us["system_clock"] = 'System Clock'
    en_us["idle_keyword"] = 'Idle Keyword'
    en_us["resume_keyword"] = 'Resume Keyword'
    en_us["idle_keyword_second"] = 'Idle Keyword (second)'
    en_us["resume_keyword_second"] = 'Resume Keyword (second)'

    en_us["status_idle"] = 'Idle'
    en_us["status_paused"] = 'Paused'
    en_us["status_enabled"] = 'Enabled'
    en_us["status_running"] = 'Running'

    en_us["idle"] = 'Idle'
    en_us["resume"] = 'Resume'

    en_us["preference"] = 'Preference'
    en_us["advanced"] = 'Advanced'
    en_us["verification_word"] = "Verification"
    en_us["maxbot_server"] = 'Server'
    en_us["autofill"] = 'Autofill'
    en_us["runtime"] = 'Runtime'
    en_us["about"] = 'About'

    en_us["run"] = 'Run'
    en_us["save"] = 'Save'
    en_us["exit"] = 'Close'
    en_us["copy"] = 'Copy'
    en_us["restore_defaults"] = 'Restore Defaults'
    en_us["config_launcher"] = 'Launcher'
    en_us["done"] = 'Done'

    en_us["tixcraft_sid"] = 'Tixcraft family cookie SID'
    en_us["ibon_ibonqware"] = 'ibon cookie ibonqware'
    en_us["facebook_account"] = 'Facebook account'
    en_us["kktix_account"] = 'KKTIX account'
    en_us["fami_account"] = 'FamiTicket account'
    en_us["cityline_account"] = 'cityline account'
    en_us["urbtix_account"] = 'URBTIX account'
    en_us["hkticketing_account"] = 'HKTICKETING account'
    en_us["kham_account"] = 'KHAM account'
    en_us["ticket_account"] = 'TICKET account'
    en_us["udn_account"] = 'UDN account'
    en_us["ticketplus_account"] = 'TicketPlus account'

    en_us["password"] = 'Password'
    en_us["facebook_password"] = 'Facebook password'
    en_us["kktix_password"] = 'KKTIX password'
    en_us["fami_password"] = 'FamiTicket password'
    en_us["cityline_password"] = 'cityline password'
    en_us["urbtix_password"] = 'URBTIX password'
    en_us["hkticketing_password"] = 'HKTICKETING password'
    en_us["kham_password"] = 'KHAM password'
    en_us["ticket_password"] = 'TICKET password'
    en_us["udn_password"] = 'UDN password'
    en_us["ticketplus_password"] = 'TicketPlus password'
    en_us["save_password_alert"] = 'Saving passwords to config file may expose your passwords.'

    en_us["play_ticket_sound"] = 'Play sound when ticketing'
    en_us["play_order_sound"] = 'Play sound when ordering'
    en_us["play_sound_filename"] = 'sound filename'

    en_us["chrome_extension"] = "Chrome Browser Extension"
    en_us["disable_adjacent_seat"] = "Disable Adjacent Seat"
    en_us["hide_some_image"] = "Hide Some Images"
    en_us["block_facebook_network"] = "Block Facebook Network"

    en_us["maxbot_slogan"] = 'MaxBot is a FREE and open source bot program. Wish you good luck.'
    en_us["donate"] = 'Donate'
    en_us["help"] = 'Help'
    en_us["release"] = 'Release'

    zh_tw = {}
    zh_tw["homepage"] = '售票網站'
    zh_tw["browser"] = '瀏覽器'
    zh_tw["language"] = '語言'
    zh_tw["ticket_number"] = '門票張數'
    zh_tw["refresh_datetime"] = '刷新在指定時間'

    zh_tw["enable"] = '啟用'
    zh_tw["recommand_enable"] = "建議啟用"
    zh_tw["auto_press_next_step_button"] = 'KKTIX點選下一步按鈕'
    zh_tw["auto_fill_ticket_number"] = '自動輸入張數'
    zh_tw["and"] = '而且（同列）'

    zh_tw["local_dictionary"] = '使用者自定字典'
    zh_tw["remote_url"] = '遠端網址'
    zh_tw["server_url"] = '伺服器網址'
    zh_tw["auto_guess_options"] = '自動猜測驗證問題'
    zh_tw["user_guess_string"] = '驗證問題中的答案清單'
    zh_tw["preview"] = '預覽'
    zh_tw["question"] = '驗證問題'
    zh_tw["answer"] = '答案'

    zh_tw["date_auto_select"] = '日期自動點選'
    zh_tw["date_select_order"] = '日期排序方式'
    zh_tw["date_keyword"] = '日期關鍵字'
    zh_tw["pass_date_is_sold_out"] = '避開「搶購一空」的日期'
    zh_tw["auto_reload_coming_soon_page"] = '自動刷新倒數中的日期頁面'
    zh_tw["auto_reload_page_interval"] = '自動刷新頁面間隔(秒)'
    zh_tw["max_dwell_time"] = 'KKTIX購票最長停留(秒)'
    zh_tw["reset_browser_interval"] = '重新啓動瀏覽器間隔(秒)'
    zh_tw["cityline_queue_retry"] = 'cityline queue retry'
    zh_tw["proxy_server_port"] = 'Proxy IP:PORT'
    zh_tw["window_size"] = '瀏覽器視窗大小'

    zh_tw["area_select_order"] = '區域排序方式'
    zh_tw["area_keyword"] = '區域關鍵字'
    zh_tw["area_auto_select"] = '區域自動點選'
    zh_tw["keyword_exclude"] = '排除關鍵字'
    zh_tw["keyword_usage"] = '每組關鍵字需要雙引號, 用逗號分隔, \n在關鍵字中使用空格作為 AND 邏輯。\n加入 ,\"\" 代表符合所有關鍵字'

    zh_tw["ocr_captcha"] = '猜測驗證碼'
    zh_tw["ocr_captcha_ddddocr_beta"] = 'ddddocr beta'
    zh_tw["ocr_captcha_force_submit"] = '掛機模式'
    zh_tw["ocr_captcha_image_source"] = 'OCR圖片取得方式'
    zh_tw["webdriver_type"] = 'WebDriver類別'
    zh_tw["headless"] = '無圖形界面模式'
    zh_tw["verbose"] = '輸出詳細除錯訊息'
    zh_tw["running_status"] = '執行狀態'
    zh_tw["running_url"] = '執行網址'
    zh_tw["system_clock"] = '系統時鐘'
    zh_tw["idle_keyword"] = '暫停關鍵字'
    zh_tw["resume_keyword"] = '接續關鍵字'
    zh_tw["idle_keyword_second"] = '暫停關鍵字(秒)'
    zh_tw["resume_keyword_second"] = '接續關鍵字(秒)'

    zh_tw["status_idle"] = '閒置中'
    zh_tw["status_paused"] = '已暫停'
    zh_tw["status_enabled"] = '已啟用'
    zh_tw["status_running"] = '執行中'

    zh_tw["idle"] = '暫停搶票'
    zh_tw["resume"] = '接續搶票'

    zh_tw["preference"] = '偏好設定'
    zh_tw["advanced"] = '進階設定'
    zh_tw["verification_word"] = "驗證問題"
    zh_tw["maxbot_server"] = '伺服器'
    zh_tw["autofill"] = '自動填表單'
    zh_tw["runtime"] = '執行階段'
    zh_tw["about"] = '關於'

    zh_tw["run"] = '搶票'
    zh_tw["save"] = '存檔'
    zh_tw["exit"] = '關閉'
    zh_tw["copy"] = '複製'
    zh_tw["restore_defaults"] = '恢復預設值'
    zh_tw["config_launcher"] = '設定檔管理'
    zh_tw["done"] = '完成'

    zh_tw["tixcraft_sid"] = '拓元家族 cookie SID'
    zh_tw["ibon_ibonqware"] = 'ibon cookie ibonqware'
    zh_tw["facebook_account"] = 'Facebook 帳號'
    zh_tw["kktix_account"] = 'KKTIX 帳號'
    zh_tw["fami_account"] = 'FamiTicket 帳號'
    zh_tw["cityline_account"] = 'cityline 帳號'
    zh_tw["urbtix_account"] = 'URBTIX 帳號'
    zh_tw["hkticketing_account"] = 'HKTICKETING 帳號'
    zh_tw["kham_account"] = '寬宏 帳號'
    zh_tw["ticket_account"] = '年代 帳號'
    zh_tw["udn_account"] = 'UDN 帳號'
    zh_tw["ticketplus_account"] = '遠大 帳號'

    zh_tw["password"] = '密碼'
    zh_tw["facebook_password"] = 'Facebook 密碼'
    zh_tw["kktix_password"] = 'KKTIX 密碼'
    zh_tw["fami_password"] = 'FamiTicket 密碼'
    zh_tw["cityline_password"] = 'cityline 密碼'
    zh_tw["urbtix_password"] = 'URBTIX 密碼'
    zh_tw["hkticketing_password"] = 'HKTICKETING 密碼'
    zh_tw["kham_password"] = '寬宏 密碼'
    zh_tw["ticket_password"] = '年代 密碼'
    zh_tw["udn_password"] = 'UDN 密碼'
    zh_tw["ticketplus_password"] = '遠大 密碼'
    zh_tw["save_password_alert"] = '將密碼保存到設定檔中可能會讓您的密碼被盜。'

    zh_tw["play_ticket_sound"] = '有票時播放音效'
    zh_tw["play_order_sound"] = '訂購時播放音效'
    zh_tw["play_sound_filename"] = '音效檔'

    zh_tw["chrome_extension"] = "Chrome 瀏覽器擴充功能"
    zh_tw["disable_adjacent_seat"] = "允許不連續座位"
    zh_tw["hide_some_image"] = "隱藏部份圖片"
    zh_tw["block_facebook_network"] = "擋掉 Facebook 連線"

    zh_tw["maxbot_slogan"] = 'MaxBot是一個免費、開放原始碼的搶票機器人。\n祝您搶票成功。'
    zh_tw["donate"] = '打賞'
    zh_tw["release"] = '所有可用版本'
    zh_tw["help"] = '使用教學'

    zh_cn = {}
    zh_cn["homepage"] = '售票网站'
    zh_cn["browser"] = '浏览器'
    zh_cn["language"] = '语言'
    zh_cn["ticket_number"] = '门票张数'
    zh_cn["refresh_datetime"] = '刷新在指定时间'

    zh_cn["enable"] = '启用'
    zh_cn["recommand_enable"] = "建议启用"

    zh_cn["auto_press_next_step_button"] = 'KKTIX自动点选下一步按钮'
    zh_cn["auto_fill_ticket_number"] = '自动输入张数'
    zh_cn["and"] = '而且（同列）'

    zh_cn["local_dictionary"] = '本地字典'
    zh_cn["remote_url"] = '远端网址'
    zh_cn["server_url"] = '服务器地址'
    zh_cn["auto_guess_options"] = '自动猜测验证问题'
    zh_cn["user_guess_string"] = '验证问题的答案列表'
    zh_cn["preview"] = '预览'
    zh_cn["question"] = '验证问题'
    zh_cn["answer"] = '答案'

    zh_cn["date_auto_select"] = '日期自动点选'
    zh_cn["date_select_order"] = '日期排序方式'
    zh_cn["date_keyword"] = '日期关键字'
    zh_cn["pass_date_is_sold_out"] = '避开“抢购一空”的日期'
    zh_cn["auto_reload_coming_soon_page"] = '自动刷新倒数中的日期页面'
    zh_cn["auto_reload_page_interval"] = '重新加载间隔(秒)'
    zh_cn["cityline_queue_retry"] = 'cityline queue retry'
    zh_cn["max_dwell_time"] = '购票网页最长停留(秒)'
    zh_cn["reset_browser_interval"] = '重新启动浏览器间隔(秒)'
    zh_cn["proxy_server_port"] = 'Proxy IP:PORT'
    zh_cn["window_size"] = '浏览器窗口大小'

    zh_cn["area_select_order"] = '区域排序方式'
    zh_cn["area_keyword"] = '区域关键字'
    zh_cn["area_auto_select"] = '区域自动点选'
    zh_cn["keyword_exclude"] = '排除关键字'
    zh_cn["keyword_usage"] = '每组关键字需要双引号, 用逗号分隔, \n在关键字中使用空格作为 AND 逻辑。\n附加 ,\"\" 以匹配所有结果。'

    zh_cn["ocr_captcha"] = '猜测验证码'
    zh_cn["ocr_captcha_ddddocr_beta"] = 'ddddocr beta'
    zh_cn["ocr_captcha_force_submit"] = '挂机模式'
    zh_cn["ocr_captcha_image_source"] = 'OCR图像源'
    zh_cn["webdriver_type"] = 'WebDriver类别'
    zh_cn["headless"] = '无图形界面模式'
    zh_cn["verbose"] = '输出详细除错讯息'
    zh_cn["running_status"] = '执行状态'
    zh_cn["running_url"] = '执行网址'
    zh_cn["system_clock"] = '系统时钟'
    zh_cn["idle_keyword"] = '暂停关键字'
    zh_cn["resume_keyword"] = '接续关键字'
    zh_cn["idle_keyword_second"] = '暂停关键字(秒)'
    zh_cn["resume_keyword_second"] = '接续关键字(秒)'

    zh_cn["status_idle"] = '闲置中'
    zh_cn["status_paused"] = '已暂停'
    zh_cn["status_enabled"] = '已启用'
    zh_cn["status_running"] = '执行中'

    zh_cn["idle"] = '暂停抢票'
    zh_cn["resume"] = '接续抢票'

    zh_cn["preference"] = '偏好设定'
    zh_cn["advanced"] = '进阶设定'
    zh_cn["verification_word"] = "验证字"
    zh_cn["maxbot_server"] = '伺服器'
    zh_cn["autofill"] = '自动填表单'
    zh_cn["runtime"] = '运行'
    zh_cn["about"] = '关于'
    zh_cn["copy"] = '复制'

    zh_cn["run"] = '抢票'
    zh_cn["save"] = '存档'
    zh_cn["exit"] = '关闭'
    zh_cn["copy"] = '复制'
    zh_cn["restore_defaults"] = '恢复默认值'
    zh_cn["config_launcher"] = '设定档管理'
    zh_cn["done"] = '完成'

    zh_cn["tixcraft_sid"] = '拓元家族 cookie SID'
    zh_cn["ibon_ibonqware"] = 'ibon cookie ibonqware'
    zh_cn["facebook_account"] = 'Facebook 帐号'
    zh_cn["kktix_account"] = 'KKTIX 帐号'
    zh_cn["fami_account"] = 'FamiTicket 帐号'
    zh_cn["cityline_account"] = 'cityline 帐号'
    zh_cn["urbtix_account"] = 'URBTIX 帐号'
    zh_cn["hkticketing_account"] = 'HKTICKETING 帐号'
    zh_cn["kham_account"] = '宽宏 帐号'
    zh_cn["ticket_account"] = '年代 帐号'
    zh_cn["udn_account"] = 'UDN 帐号'
    zh_cn["ticketplus_account"] = '远大 帐号'

    zh_cn["password"] = '密码'
    zh_cn["facebook_password"] = 'Facebook 密码'
    zh_cn["kktix_password"] = 'KKTIX 密码'
    zh_cn["fami_password"] = 'FamiTicket 密码'
    zh_cn["cityline_password"] = 'cityline 密码'
    zh_cn["urbtix_password"] = 'URBTIX 密码'
    zh_cn["hkticketing_password"] = 'HKTICKETING 密码'
    zh_cn["kham_password"] = '宽宏 密码'
    zh_cn["ticket_password"] = '年代 密码'
    zh_cn["udn_password"] = 'UDN 密码'
    zh_cn["ticketplus_password"] = '远大 密码'
    zh_cn["save_password_alert"] = '将密码保存到文件中可能会暴露您的密码。'

    zh_cn["play_ticket_sound"] = '有票时播放音效'
    zh_cn["play_order_sound"] = '订购时播放音效'
    zh_cn["play_sound_filename"] = '音效档'

    zh_cn["chrome_extension"] = "Chrome 浏览器扩展程序"
    zh_cn["disable_adjacent_seat"] = "允许不连续座位"
    zh_cn["hide_some_image"] = "隐藏一些图像"
    zh_cn["block_facebook_network"] = "擋掉 Facebook 連線"

    zh_cn["maxbot_slogan"] = 'MaxBot 是一个免费的开源机器人程序。\n祝您抢票成功。'
    zh_cn["donate"] = '打赏'
    zh_cn["help"] = '使用教学'
    zh_cn["release"] = '所有可用版本'

    ja_jp = {}
    ja_jp["homepage"] = 'ホームページ'
    ja_jp["browser"] = 'ブラウザ'
    ja_jp["language"] = '言語'
    ja_jp["ticket_number"] = '枚数'
    ja_jp["refresh_datetime"] = '目標時間にリフレッシュ'

    ja_jp["enable"] = '有効'
    ja_jp["recommand_enable"] = "有効化を推奨"

    ja_jp["auto_press_next_step_button"] = 'KKTIX次を自動で押す'
    ja_jp["auto_fill_ticket_number"] = '枚数自動入力'
    ja_jp["and"] = 'そして（同列）'

    ja_jp["local_dictionary"] = 'ローカル辞書'
    ja_jp["remote_url"] = 'リモートURL'
    ja_jp["server_url"] = 'サーバーURL'
    ja_jp["auto_guess_options"] = '自動推測検証問題'
    ja_jp["user_guess_string"] = '検証用の質問の回答リスト'
    ja_jp["preview"] = 'プレビュー'
    ja_jp["question"] = '質問'
    ja_jp["answer"] = '答え'

    ja_jp["date_auto_select"] = '日付自動選択'
    ja_jp["date_select_order"] = '日付のソート方法'
    ja_jp["date_keyword"] = '日付キーワード'
    ja_jp["pass_date_is_sold_out"] = '「売り切れ」公演を避ける'
    ja_jp["auto_reload_coming_soon_page"] = '公開予定のページをリロード'
    ja_jp["auto_reload_page_interval"] = 'リロード間隔(秒)'
    ja_jp["max_dwell_time"] = '最大滞留時間(秒)'
    ja_jp["cityline_queue_retry"] = 'cityline queue retry'
    ja_jp["reset_browser_interval"] = 'ブラウザの再起動間隔（秒）'
    ja_jp["proxy_server_port"] = 'Proxy IP:PORT'
    ja_jp["window_size"] = 'ウィンドウサイズ'

    ja_jp["area_select_order"] = 'エリアソート方法'
    ja_jp["area_keyword"] = 'エリアキーワード'
    ja_jp["area_auto_select"] = 'エリア自動選択'
    ja_jp["keyword_exclude"] = '除外キーワード'
    ja_jp["keyword_usage"] = '各キーワードはカンマで区切られた二重引用符が必要です。\nキーワード内のスペースを AND ロジックとして使用します。\nすべてに一致するように ,\"\" を追加します。'

    ja_jp["ocr_captcha"] = 'キャプチャを推測する'
    ja_jp["ocr_captcha_ddddocr_beta"] = 'ddddocr beta'
    ja_jp["ocr_captcha_force_submit"] = 'キーボードから離れて'
    ja_jp["ocr_captcha_image_source"] = 'OCR 画像ソース'
    ja_jp["webdriver_type"] = 'WebDriverタイプ'
    ja_jp["headless"] = 'ヘッドレスモード'
    ja_jp["verbose"] = '詳細モード'
    ja_jp["running_status"] = 'スターテス'
    ja_jp["running_url"] = '現在の URL'
    ja_jp["system_clock"] = 'システムクロック'
    ja_jp["idle_keyword"] = 'アイドルキーワード'
    ja_jp["resume_keyword"] = '再起動キーワード'
    ja_jp["idle_keyword_second"] = 'アイドルキーワード（秒）'
    ja_jp["resume_keyword_second"] = '再起動キーワード（秒）'

    ja_jp["status_idle"] = 'アイドル状態'
    ja_jp["status_paused"] = '一時停止'
    ja_jp["status_enabled"] = '有効'
    ja_jp["status_running"] = 'ランニング'

    ja_jp["idle"] = 'アイドル'
    ja_jp["resume"] = '再起動'

    ja_jp["preference"] = '設定'
    ja_jp["advanced"] = '高度な設定'
    ja_jp["verification_word"] = "確認の言葉"
    ja_jp["maxbot_server"] = 'サーバ'
    ja_jp["autofill"] = 'オートフィル'
    ja_jp["runtime"] = 'ランタイム'
    ja_jp["about"] = '情報'

    ja_jp["run"] = 'チケットを取る'
    ja_jp["save"] = '保存'
    ja_jp["exit"] = '閉じる'
    ja_jp["copy"] = 'コピー'
    ja_jp["restore_defaults"] = 'デフォルトに戻す'
    ja_jp["config_launcher"] = 'ランチャー'
    ja_jp["done"] = '終わり'

    ja_jp["tixcraft_sid"] = '拓元家 cookie SID'
    ja_jp["ibon_ibonqware"] = 'ibon cookie ibonqware'
    ja_jp["facebook_account"] = 'Facebookのアカウント'
    ja_jp["kktix_account"] = 'KKTIXのアカウント'
    ja_jp["fami_account"] = 'FamiTicketのアカウント'
    ja_jp["cityline_account"] = 'citylineのアカウント'
    ja_jp["urbtix_account"] = 'URBTIXのアカウント'
    ja_jp["hkticketing_account"] = 'HKTICKETINGのアカウント'
    ja_jp["kham_account"] = 'KHAMのアカウント'
    ja_jp["ticket_account"] = 'TICKETのアカウント'
    ja_jp["udn_account"] = 'UDNのアカウント'
    ja_jp["ticketplus_account"] = '遠大のアカウント'

    ja_jp["password"] = 'パスワード'
    ja_jp["facebook_password"] = 'Facebookのパスワード'
    ja_jp["kktix_password"] = 'KKTIXのパスワード'
    ja_jp["fami_password"] = 'FamiTicketのパスワード'
    ja_jp["cityline_password"] = 'citylineのパスワード'
    ja_jp["urbtix_password"] = 'URBTIXのパスワード'
    ja_jp["hkticketing_password"] = 'HKTICKETINGのパスワード'
    ja_jp["kham_password"] = 'KHAMのパスワード'
    ja_jp["ticket_password"] = 'TICKETのパスワード'
    ja_jp["udn_password"] = 'UDNのパスワード'
    ja_jp["ticketplus_password"] = '遠大のパスワード'
    ja_jp["save_password_alert"] = 'パスワードをファイルに保存すると、パスワードが公開される可能性があります。'

    ja_jp["play_ticket_sound"] = '有票時に音を鳴らす'
    ja_jp["play_order_sound"] = '注文時に音を鳴らす'
    ja_jp["play_sound_filename"] = 'サウンドファイル'

    ja_jp["chrome_extension"] = "Chrome ブラウザ拡張機能"
    ja_jp["disable_adjacent_seat"] = "連続しない座席も可"
    ja_jp["hide_some_image"] = "一部の画像を非表示にする"
    ja_jp["block_facebook_network"] = "Facebookをブロックする"

    ja_jp["maxbot_slogan"] = 'MaxBot は無料のオープン ソース ボット プログラムです。チケットの成功をお祈りします。'
    ja_jp["donate"] = '寄付'
    ja_jp["help"] = '利用方法'
    ja_jp["release"] = 'リリース'

    translate['en_us'] = en_us
    translate['zh_tw'] = zh_tw
    translate['zh_cn'] = zh_cn
    translate['ja_jp'] = ja_jp
    return translate


def get_default_config():
    config_dict = {}

    config_dict["homepage"] = CONST_HOMEPAGE_DEFAULT
    config_dict["browser"] = "chrome"
    config_dict["language"] = "English"
    config_dict["ticket_number"] = 2
    config_dict["refresh_datetime"] = ""

    config_dict["ocr_captcha"] = {}
    config_dict["ocr_captcha"]["enable"] = True
    config_dict["ocr_captcha"]["beta"] = True
    config_dict["ocr_captcha"]["force_submit"] = True
    config_dict["ocr_captcha"]["image_source"] = CONST_OCR_CAPTCH_IMAGE_SOURCE_CANVAS
    config_dict["webdriver_type"] = CONST_WEBDRIVER_TYPE_UC

    config_dict["date_auto_select"] = {}
    config_dict["date_auto_select"]["enable"] = True
    config_dict["date_auto_select"]["date_keyword"] = ""
    config_dict["date_auto_select"]["mode"] = CONST_SELECT_ORDER_DEFAULT

    config_dict["area_auto_select"] = {}
    config_dict["area_auto_select"]["enable"] = True
    config_dict["area_auto_select"]["mode"] = CONST_SELECT_ORDER_DEFAULT
    config_dict["area_auto_select"]["area_keyword"] = ""
    config_dict["keyword_exclude"] = CONST_EXCLUDE_DEFAULT

    config_dict['kktix'] = {}
    config_dict["kktix"]["auto_press_next_step_button"] = True
    config_dict["kktix"]["auto_fill_ticket_number"] = True
    config_dict["kktix"]["max_dwell_time"] = 60

    config_dict['cityline'] = {}
    config_dict["cityline"]["cityline_queue_retry"] = True

    config_dict['tixcraft'] = {}
    config_dict["tixcraft"]["pass_date_is_sold_out"] = True
    config_dict["tixcraft"]["auto_reload_coming_soon_page"] = True

    config_dict['advanced'] = {}

    config_dict['advanced']['play_sound'] = {}
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
    config_dict["advanced"]["remote_url"] = "http://127.0.0.1:%d/" % (CONST_SERVER_PORT)

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


def read_last_url_from_file():
    ret = ""
    if os.path.exists(CONST_MAXBOT_LAST_URL_FILE):
        try:
            with open(CONST_MAXBOT_LAST_URL_FILE, "r") as text_file:
                ret = text_file.readline()
        except Exception as e:
            pass
    return ret


def load_json():
    app_root = system_tool.get_curr_process_work_root_dir()

    # overwrite config path.
    config_filepath = os.path.join(app_root, CONST_MAXBOT_CONFIG_FILE_NAME)

    config_dict = None
    if os.path.isfile(config_filepath):
        try:
            with open(config_filepath) as json_data:
                config_dict = json.load(json_data)
        except Exception as e:
            pass
    else:
        config_dict = get_default_config()
    return config_filepath, config_dict


def btn_restore_defaults_clicked():
    app_root = system_tool.get_curr_process_work_root_dir()
    config_filepath = os.path.join(app_root, CONST_MAXBOT_CONFIG_FILE_NAME)
    if os.path.exists(str(config_filepath)):
        try:
            os.unlink(str(config_filepath))
        except Exception as exc:
            print(exc)
            pass

    config_dict = get_default_config()
    language_code = get_language_code_by_name(config_dict["language"])

    messagebox.showinfo(translate[language_code]["restore_defaults"], translate[language_code]["done"])

    global root
    load_GUI(root, config_dict)


def do_maxbot_idle():
    app_root = system_tool.get_curr_process_work_root_dir()
    idle_filepath = os.path.join(app_root, CONST_MAXBOT_INT28_FILE)
    try:
        with open(CONST_MAXBOT_INT28_FILE, "w") as text_file:
            text_file.write("")
    except Exception as e:
        pass


def btn_idle_clicked(language_code):
    do_maxbot_idle()
    update_maxbot_runtime_status()


def do_maxbot_resume():
    app_root = system_tool.get_curr_process_work_root_dir()
    idle_filepath = os.path.join(app_root, CONST_MAXBOT_INT28_FILE)
    for i in range(3):
        util.force_remove_file(idle_filepath)


def btn_resume_clicked(language_code):
    do_maxbot_resume()
    update_maxbot_runtime_status()


def btn_launcher_clicked():
    Root_Dir = ""
    save_ret = btn_save_act(slience_mode=True)
    if save_ret:
        script_name = "config_launcher"
        threading.Thread(target=util.launch_maxbot, args=(script_name,)).start()


def btn_save_clicked():
    btn_save_act()


def btn_save_act(slience_mode=False):
    app_root = system_tool.get_curr_process_work_root_dir()
    config_filepath = os.path.join(app_root, CONST_MAXBOT_CONFIG_FILE_NAME)

    config_dict = get_default_config()
    language_code = get_language_code_by_name(config_dict["language"])

    # read user input
    global combo_homepage
    global combo_browser
    global combo_language
    global combo_ticket_number

    global chk_state_auto_press_next_step_button
    global chk_state_auto_fill_ticket_number
    global txt_user_guess_string

    global chk_state_date_auto_select
    global txt_date_keyword
    global chk_state_area_auto_select
    global txt_area_keyword
    global txt_keyword_exclude
    global txt_remote_url

    global combo_date_auto_select_mode
    global combo_area_auto_select_mode

    global chk_state_pass_date_is_sold_out
    global chk_state_auto_reload_coming_soon_page
    global txt_auto_reload_page_interval
    global txt_max_dwell_time
    global chk_status_cityline_queue_retry
    global txt_reset_browser_intervalv
    global txt_proxy_server_port
    global txt_window_size

    global txt_tixcraft_sid
    global txt_ibon_ibonqware
    global txt_facebook_account
    global txt_kktix_account
    global txt_fami_account
    global txt_cityline_account
    global txt_urbtix_account
    global txt_hkticketing_account
    global txt_kham_account
    global txt_ticket_account
    global txt_udn_account
    global txt_ticketplus_account

    global txt_facebook_password
    global txt_kktix_password
    global txt_fami_password
    global txt_cityline_password
    global txt_urbtix_password
    global txt_hkticketing_password
    global txt_kham_password
    global txt_ticket_password
    global txt_udn_password
    global txt_ticketplus_password

    global chk_state_play_ticket_sound
    global chk_state_play_order_sound
    global txt_play_sound_filename
    global chk_state_ocr_captcha
    global chk_state_ocr_captcha_ddddocr_beta
    global chk_state_ocr_captcha_force_submit
    global chk_state_chrome_extension
    global chk_state_adjacent_seat
    global chk_state_hide_some_image
    global chk_state_block_facebook_network

    global chk_state_headless
    global chk_state_verbose
    global chk_state_auto_guess_options
    global combo_ocr_captcha_image_source
    global combo_webdriver_type

    global txt_idle_keyword
    global txt_resume_keyword
    global txt_idle_keyword_second
    global txt_resume_keyword_second

    is_all_data_correct = True

    if is_all_data_correct:
        if combo_homepage.get().strip() == "":
            is_all_data_correct = False
            messagebox.showerror("Error", "Please enter homepage")
        else:
            homepage_domain = combo_homepage.get().strip()
            if ' (' in homepage_domain:
                homepage_domain = homepage_domain.split(' (')[0]
            config_dict["homepage"] = homepage_domain

    if is_all_data_correct:
        if combo_browser.get().strip() == "":
            is_all_data_correct = False
            messagebox.showerror("Error", "Please select a browser: chrome or firefox")
        else:
            config_dict["browser"] = combo_browser.get().strip()

    if is_all_data_correct:
        if combo_language.get().strip() == "":
            is_all_data_correct = False
            messagebox.showerror("Error", "Please select a language")
        else:
            config_dict["language"] = combo_language.get().strip()
            # display as new language.
            language_code = get_language_code_by_name(config_dict["language"])

    if is_all_data_correct:
        if combo_ticket_number.get().strip() == "":
            is_all_data_correct = False
            messagebox.showerror("Error", "Please select a value")
        else:
            config_dict["ticket_number"] = int(combo_ticket_number.get().strip())

    if is_all_data_correct:
        config_dict["kktix"]["auto_press_next_step_button"] = bool(chk_state_auto_press_next_step_button.get())
        config_dict["kktix"]["auto_fill_ticket_number"] = bool(chk_state_auto_fill_ticket_number.get())

        config_dict["kktix"]["max_dwell_time"] = int(txt_max_dwell_time.get().strip())
        if config_dict["kktix"]["max_dwell_time"] > 0:
            if config_dict["kktix"]["max_dwell_time"] < 15:
                config_dict["kktix"]["max_dwell_time"] = 15

        config_dict["cityline"]["cityline_queue_retry"] = bool(chk_state_cityline_queue_retry.get())

        config_dict["date_auto_select"]["enable"] = bool(chk_state_date_auto_select.get())
        config_dict["date_auto_select"]["mode"] = combo_date_auto_select_mode.get().strip()

        date_keyword = txt_date_keyword.get("1.0", END).strip()
        date_keyword = util.format_config_keyword_for_json(date_keyword)
        config_dict["date_auto_select"]["date_keyword"] = date_keyword

        config_dict["tixcraft"]["pass_date_is_sold_out"] = bool(chk_state_pass_date_is_sold_out.get())
        config_dict["tixcraft"]["auto_reload_coming_soon_page"] = bool(chk_state_auto_reload_coming_soon_page.get())

        area_keyword = txt_area_keyword.get("1.0", END).strip()
        area_keyword = util.format_config_keyword_for_json(area_keyword)

        keyword_exclude = txt_keyword_exclude.get("1.0", END).strip()
        keyword_exclude = util.format_config_keyword_for_json(keyword_exclude)

        user_guess_string = txt_user_guess_string.get("1.0", END).strip()
        user_guess_string = util.format_config_keyword_for_json(user_guess_string)

        remote_url = txt_remote_url.get("1.0", END).strip()
        remote_url = util.format_config_keyword_for_json(remote_url)

        idle_keyword = txt_idle_keyword.get("1.0", END).strip()
        idle_keyword = util.format_config_keyword_for_json(idle_keyword)

        resume_keyword = txt_resume_keyword.get("1.0", END).strip()
        resume_keyword = util.format_config_keyword_for_json(resume_keyword)

        idle_keyword_second = txt_idle_keyword_second.get("1.0", END).strip()
        idle_keyword_second = util.format_config_keyword_for_json(idle_keyword_second)

        resume_keyword_second = txt_resume_keyword_second.get("1.0", END).strip()
        resume_keyword_second = util.format_config_keyword_for_json(resume_keyword_second)

        # test keyword format.
        if is_all_data_correct:
            if len(area_keyword) > 0:
                try:
                    test_array = json.loads("[" + area_keyword + "]")
                except Exception as exc:
                    print(exc)
                    messagebox.showinfo(translate[language_code]["save"],
                                        "Error:" + translate[language_code]["area_keyword"])
                    is_all_data_correct = False

        if is_all_data_correct:
            if len(keyword_exclude) > 0:
                try:
                    test_array = json.loads("[" + keyword_exclude + "]")
                except Exception as exc:
                    print(exc)
                    messagebox.showinfo(translate[language_code]["save"],
                                        "Error:" + translate[language_code]["keyword_exclude"])
                    is_all_data_correct = False

        if is_all_data_correct:
            if len(user_guess_string) > 0:
                try:
                    test_array = json.loads("[" + user_guess_string + "]")
                except Exception as exc:
                    print(exc)
                    messagebox.showinfo(translate[language_code]["save"],
                                        "Error:" + translate[language_code]["user_guess_string"])
                    is_all_data_correct = False

        if is_all_data_correct:
            if len(remote_url) > 0:
                try:
                    test_array = json.loads("[" + remote_url + "]")
                except Exception as exc:
                    print(exc)
                    messagebox.showinfo(translate[language_code]["save"],
                                        "Error:" + translate[language_code]["remote_url"])
                    is_all_data_correct = False

        if is_all_data_correct:
            if len(idle_keyword) > 0:
                try:
                    test_array = json.loads("[" + idle_keyword + "]")
                except Exception as exc:
                    print(exc)
                    messagebox.showinfo(translate[language_code]["save"],
                                        "Error:" + translate[language_code]["idle_keyword"])
                    is_all_data_correct = False

        if is_all_data_correct:
            if len(resume_keyword) > 0:
                try:
                    test_array = json.loads("[" + resume_keyword + "]")
                except Exception as exc:
                    print(exc)
                    messagebox.showinfo(translate[language_code]["save"],
                                        "Error:" + translate[language_code]["resume_keyword"])
                    is_all_data_correct = False

        if is_all_data_correct:
            if len(idle_keyword_second) > 0:
                try:
                    test_array = json.loads("[" + idle_keyword_second + "]")
                except Exception as exc:
                    print(exc)
                    messagebox.showinfo(translate[language_code]["save"],
                                        "Error:" + translate[language_code]["idle_keyword_second"])
                    is_all_data_correct = False

        if is_all_data_correct:
            if len(resume_keyword_second) > 0:
                try:
                    test_array = json.loads("[" + resume_keyword_second + "]")
                except Exception as exc:
                    print(exc)
                    messagebox.showinfo(translate[language_code]["save"],
                                        "Error:" + translate[language_code]["resume_keyword_second"])
                    is_all_data_correct = False

        if is_all_data_correct:
            config_dict["area_auto_select"]["area_keyword"] = area_keyword
            config_dict["keyword_exclude"] = keyword_exclude
            config_dict["advanced"]["user_guess_string"] = user_guess_string
            config_dict["advanced"]["remote_url"] = remote_url

            config_dict["advanced"]["idle_keyword"] = idle_keyword
            config_dict["advanced"]["resume_keyword"] = resume_keyword
            config_dict["advanced"]["idle_keyword_second"] = idle_keyword_second
            config_dict["advanced"]["resume_keyword_second"] = resume_keyword_second

            txt_idle_keyword.delete(1.0, "end")
            txt_resume_keyword.delete(1.0, "end")
            txt_idle_keyword_second.delete(1.0, "end")
            txt_resume_keyword_second.delete(1.0, "end")

            txt_idle_keyword.insert("1.0", config_dict["advanced"]["idle_keyword"].strip())
            txt_resume_keyword.insert("1.0", config_dict["advanced"]["resume_keyword"].strip())
            txt_idle_keyword_second.insert("1.0", config_dict["advanced"]["idle_keyword_second"].strip())
            txt_resume_keyword_second.insert("1.0", config_dict["advanced"]["resume_keyword_second"].strip())

    if is_all_data_correct:
        config_dict["refresh_datetime"] = txt_refresh_datetime.get().strip()
        config_dict["area_auto_select"]["enable"] = bool(chk_state_area_auto_select.get())
        config_dict["area_auto_select"]["mode"] = combo_area_auto_select_mode.get().strip()

        config_dict["advanced"]["play_sound"]["ticket"] = bool(chk_state_play_ticket_sound.get())
        config_dict["advanced"]["play_sound"]["order"] = bool(chk_state_play_order_sound.get())
        config_dict["advanced"]["play_sound"]["filename"] = txt_play_sound_filename.get().strip()

        config_dict["advanced"]["tixcraft_sid"] = txt_tixcraft_sid.get().strip()
        config_dict["advanced"]["ibonqware"] = txt_ibon_ibonqware.get().strip()

        config_dict["advanced"]["facebook_account"] = txt_facebook_account.get().strip()
        config_dict["advanced"]["kktix_account"] = txt_kktix_account.get().strip()
        config_dict["advanced"]["fami_account"] = txt_fami_account.get().strip()
        config_dict["advanced"]["cityline_account"] = txt_cityline_account.get().strip()
        config_dict["advanced"]["urbtix_account"] = txt_urbtix_account.get().strip()
        config_dict["advanced"]["hkticketing_account"] = txt_hkticketing_account.get().strip()
        config_dict["advanced"]["kham_account"] = txt_kham_account.get().strip()
        config_dict["advanced"]["ticket_account"] = txt_ticket_account.get().strip()
        config_dict["advanced"]["udn_account"] = txt_udn_account.get().strip()
        config_dict["advanced"]["ticketplus_account"] = txt_ticketplus_account.get().strip()

        config_dict["advanced"]["facebook_password"] = txt_facebook_password.get().strip()
        config_dict["advanced"]["kktix_password"] = txt_kktix_password.get().strip()
        config_dict["advanced"]["fami_password"] = txt_fami_password.get().strip()
        config_dict["advanced"]["cityline_password"] = txt_cityline_password.get().strip()
        config_dict["advanced"]["urbtix_password"] = txt_urbtix_password.get().strip()
        config_dict["advanced"]["hkticketing_password"] = txt_hkticketing_password.get().strip()
        config_dict["advanced"]["kham_password"] = txt_kham_password.get().strip()
        config_dict["advanced"]["ticket_password"] = txt_ticket_password.get().strip()
        config_dict["advanced"]["udn_password"] = txt_udn_password.get().strip()
        config_dict["advanced"]["ticketplus_password"] = txt_ticketplus_password.get().strip()

        config_dict["advanced"]["tixcraft_sid"] = config_dict["advanced"]["tixcraft_sid"]
        config_dict["advanced"]["ibonqware"] = config_dict["advanced"]["ibonqware"]

        config_dict["advanced"]["facebook_password"] = util.encryptMe(config_dict["advanced"]["facebook_password"])
        config_dict["advanced"]["kktix_password"] = util.encryptMe(config_dict["advanced"]["kktix_password"])
        config_dict["advanced"]["fami_password"] = util.encryptMe(config_dict["advanced"]["fami_password"])
        config_dict["advanced"]["cityline_password"] = util.encryptMe(config_dict["advanced"]["cityline_password"])
        config_dict["advanced"]["urbtix_password"] = util.encryptMe(config_dict["advanced"]["urbtix_password"])
        config_dict["advanced"]["hkticketing_password"] = util.encryptMe(
            config_dict["advanced"]["hkticketing_password"])
        config_dict["advanced"]["kham_password"] = util.encryptMe(config_dict["advanced"]["kham_password"])
        config_dict["advanced"]["ticket_password"] = util.encryptMe(config_dict["advanced"]["ticket_password"])
        config_dict["advanced"]["udn_password"] = util.encryptMe(config_dict["advanced"]["udn_password"])
        config_dict["advanced"]["ticketplus_password"] = util.encryptMe(config_dict["advanced"]["ticketplus_password"])

        config_dict["advanced"]["chrome_extension"] = bool(chk_state_chrome_extension.get())
        config_dict["advanced"]["disable_adjacent_seat"] = bool(chk_state_adjacent_seat.get())
        config_dict["advanced"]["hide_some_image"] = bool(chk_state_hide_some_image.get())
        config_dict["advanced"]["block_facebook_network"] = bool(chk_state_block_facebook_network.get())

        config_dict["ocr_captcha"] = {}
        config_dict["ocr_captcha"]["enable"] = bool(chk_state_ocr_captcha.get())
        config_dict["ocr_captcha"]["beta"] = bool(chk_state_ocr_captcha_ddddocr_beta.get())
        config_dict["ocr_captcha"]["force_submit"] = bool(chk_state_ocr_captcha_force_submit.get())
        config_dict["ocr_captcha"]["image_source"] = combo_ocr_captcha_image_source.get().strip()

        config_dict["webdriver_type"] = combo_webdriver_type.get().strip()
        config_dict["advanced"]["headless"] = bool(chk_state_headless.get())
        # config_dict["advanced"]["verbose"] = bool(chk_state_verbose.get())

        config_dict["advanced"]["auto_guess_options"] = bool(chk_state_auto_guess_options.get())

        config_dict["advanced"]["auto_reload_page_interval"] = float(txt_auto_reload_page_interval.get().strip())
        config_dict["advanced"]["reset_browser_interval"] = int(txt_reset_browser_interval.get().strip())
        config_dict["advanced"]["proxy_server_port"] = txt_proxy_server_port.get().strip()
        config_dict["advanced"]["window_size"] = txt_window_size.get().strip()

        if config_dict["advanced"]["reset_browser_interval"] > 0:
            if config_dict["advanced"]["reset_browser_interval"] < 20:
                # min value is 20 seconds.
                config_dict["advanced"]["reset_browser_interval"] = 20

    # save config.
    if is_all_data_correct:
        if not slience_mode:
            # messagebox.showinfo(translate[language_code]["save"], translate[language_code]["done"])
            file_to_save = asksaveasfilename(initialdir=app_root, initialfile=CONST_MAXBOT_CONFIG_FILE_NAME,
                                             defaultextension=".json",
                                             filetypes=[("json Documents", "*.json"), ("All Files", "*.*")])
            if not file_to_save is None:
                if len(file_to_save) > 0:
                    print("save as to:", file_to_save)
                    util.save_json(config_dict, file_to_save)
        else:
            # slience
            util.save_json(config_dict, config_filepath)

    return is_all_data_correct


def btn_run_clicked():
    print('[*INFO*] - run button pressed.')
    Root_Dir = ""
    save_ret = btn_save_act(slience_mode=True)
    print("[*INFO*] - save config result:", save_ret)
    if save_ret:
        launch_maxbot()


def launch_maxbot():
    global launch_counter
    if "launch_counter" in globals():
        launch_counter += 1
    else:
        launch_counter = 0

    webdriver_type = ""
    global combo_webdriver_type
    if 'combo_webdriver_type' in globals():
        webdriver_type = combo_webdriver_type.get().strip()

    script_name = "chrome_tixcraft"
    if webdriver_type == CONST_WEBDRIVER_TYPE_NODRIVER:
        script_name = "nodriver_tixcraft"

    msg = f"[*INFO*] - triggered script_name: {script_name}"
    print(msg)

    global txt_window_size
    window_size = txt_window_size.get().strip()
    if len(window_size) > 0:
        if "," in window_size:
            size_array = window_size.split(",")
            target_width = int(size_array[0])
            target_left = target_width * launch_counter
            # print("target_left:", target_left)
            if target_left >= 1440:
                launch_counter = 0
            window_size = window_size + "," + str(launch_counter)
            # print("window_size:", window_size)

    threading.Thread(
        target=util.launch_maxbot,
        args=(script_name, "", "", "", "", window_size,)
    ).start()


def show_preview_text():
    if os.path.exists(CONST_MAXBOT_ANSWER_ONLINE_FILE):
        answer_text = ""
        try:
            with open(CONST_MAXBOT_ANSWER_ONLINE_FILE, "r") as text_file:
                answer_text = text_file.readline()
        except Exception as e:
            pass

        if len(answer_text) > 0:
            answer_text = util.format_config_keyword_for_json(answer_text)

        date_array = []
        try:
            date_array = json.loads("[" + answer_text + "]")
        except Exception as exc:
            date_array = []

        if len(date_array) > 0:
            preview_string = text = ','.join(date_array)
            global lbl_online_dictionary_preview_data
            if 'lbl_online_dictionary_preview_data' in globals():
                try:
                    lbl_online_dictionary_preview_data.config(preview_string)
                except Exception as exc:
                    pass


def btn_preview_text_clicked():
    global txt_remote_url
    remote_url = ""
    if 'txt_remote_url' in globals():
        try:
            remote_url = txt_remote_url.get("1.0", END).strip()
        except Exception as exc:
            pass
    remote_url = util.format_config_keyword_for_json(remote_url)

    if len(remote_url) > 0:
        url_array = []
        try:
            url_array = json.loads("[" + remote_url + "]")
        except Exception as exc:
            url_array = []

        force_write = False
        if len(url_array) > 0:
            if len(url_array) == 1:
                force_write = True
            for each_url in url_array:
                # print("new_remote_url:", new_remote_url)
                is_write_to_file = util.save_url_to_file(each_url, CONST_MAXBOT_ANSWER_ONLINE_FILE,
                                                         force_write=force_write)
                if is_write_to_file:
                    break
    show_preview_text()


def btn_open_text_server_clicked():
    global tab4
    global tabControl
    tabControl.select(tab4)


def btn_preview_sound_clicked():
    global txt_play_sound_filename
    new_sound_filename = txt_play_sound_filename.get().strip()
    # print("new_sound_filename:", new_sound_filename)
    app_root = system_tool.get_curr_process_work_root_dir()
    new_sound_filename = os.path.join(app_root, new_sound_filename)
    util.play_mp3_async(new_sound_filename)


def open_url(url):
    webbrowser.open_new(url)


def btn_exit_clicked():
    root.destroy()


def btn_donate_clicked():
    webbrowser.open(URL_DONATE)


def btn_help_clicked():
    webbrowser.open(URL_HELP)


def callbackLanguageOnChange(event):
    applyNewLanguage()


def get_language_code_by_name(new_language):
    language_code = "en_us"
    if u'繁體中文' in new_language:
        language_code = 'zh_tw'
    if u'簡体中文' in new_language:
        language_code = 'zh_cn'
    if u'日本語' in new_language:
        language_code = 'ja_jp'
    # print("new language code:", language_code)

    return language_code


def applyNewLanguage():
    global combo_language
    new_language = combo_language.get().strip()
    # print("new language value:", new_language)

    language_code = get_language_code_by_name(new_language)

    global lbl_homepage
    global lbl_browser
    global lbl_language
    global lbl_ticket_number
    global lbl_refresh_datetime

    # for kktix
    global lbl_auto_press_next_step_button
    global lbl_auto_fill_ticket_number
    global lbl_user_guess_string_description
    global lbl_user_guess_string

    # for tixcraft
    global lbl_date_auto_select
    global lbl_date_auto_select_mode
    global lbl_date_keyword
    global lbl_area_auto_select
    global lbl_area_auto_select_mode
    global lbl_area_keyword
    global lbl_keyword_exclude
    global lbl_keyword_usage

    global lbl_pass_date_is_sold_out
    global lbl_auto_reload_coming_soon_page
    global lbl_ocr_captcha
    global lbl_ocr_captcha_ddddocr_beta
    global lbl_ocr_captcha_force_submit
    global lbl_ocr_captcha_image_source
    global lbl_webdriver_type
    global lbl_headless
    global lbl_verbose
    global lbl_auto_guess_options

    global lbl_maxbot_status
    global lbl_maxbot_last_url
    global lbl_system_clock
    global lbl_idle_keyword
    global lbl_resume_keyword
    global lbl_idle_keyword_second
    global lbl_resume_keyword_second

    # for checkbox
    global chk_auto_press_next_step_button
    global chk_auto_fill_ticket_number
    global chk_date_auto_select
    global chk_area_auto_select
    global chk_pass_date_is_sold_out
    global chk_auto_reload_coming_soon_page
    global chk_play_ticket_sound
    global chk_play_order_sound
    global chk_ocr_captcha
    global chk_ocr_captcha_ddddocr_beta
    global chk_ocr_captcha_force_submit
    global chk_chrome_extension
    global chk_adjacent_seat
    global chk_hide_some_image
    global chk_block_facebook_network

    global chk_headless
    global chk_verbose
    global lbl_remote_url
    global lbl_server_url
    global lbl_online_dictionary_preview
    global lbl_question
    global lbl_answer
    global chk_auto_guess_options

    global tabControl

    global lbl_slogan
    global lbl_help
    global lbl_donate
    global lbl_release

    global lbl_chrome_extension
    global lbl_adjacent_seat
    global lbl_hide_some_image
    global lbl_block_facebook_network

    global lbl_hide_some_image_recommand
    global lbl_block_facebook_network_recommand

    global lbl_auto_reload_page_interval
    global lbl_max_dwell_time
    global lbl_cityline_queue_retry
    global chk_cityline_queue_retry
    global lbl_reset_browser_interval
    global lbl_proxy_server_port
    global lbl_window_size

    lbl_homepage.config(text=translate[language_code]["homepage"])
    lbl_browser.config(text=translate[language_code]["browser"])
    lbl_language.config(text=translate[language_code]["language"])
    lbl_ticket_number.config(text=translate[language_code]["ticket_number"])
    lbl_refresh_datetime.config(text=translate[language_code]["refresh_datetime"])

    lbl_auto_press_next_step_button.config(text=translate[language_code]["auto_press_next_step_button"])
    lbl_auto_fill_ticket_number.config(text=translate[language_code]["auto_fill_ticket_number"])
    lbl_user_guess_string_description.config(text=translate[language_code]["user_guess_string"])
    lbl_user_guess_string.config(text=translate[language_code]["local_dictionary"])

    lbl_date_auto_select.config(text=translate[language_code]["date_auto_select"])
    lbl_date_auto_select_mode.config(text=translate[language_code]["date_select_order"])
    lbl_date_keyword.config(text=translate[language_code]["date_keyword"])
    lbl_area_auto_select.config(text=translate[language_code]["area_auto_select"])
    lbl_area_auto_select_mode.config(text=translate[language_code]["area_select_order"])
    lbl_area_keyword.config(text=translate[language_code]["area_keyword"])
    lbl_keyword_exclude.config(text=translate[language_code]["keyword_exclude"])
    lbl_keyword_usage.config(text=translate[language_code]["keyword_usage"])
    lbl_pass_date_is_sold_out.config(text=translate[language_code]["pass_date_is_sold_out"])
    lbl_auto_reload_coming_soon_page.config(text=translate[language_code]["auto_reload_coming_soon_page"])
    lbl_ocr_captcha.config(text=translate[language_code]["ocr_captcha"])
    lbl_ocr_captcha_ddddocr_beta.config(text=translate[language_code]["ocr_captcha_ddddocr_beta"])
    lbl_ocr_captcha_force_submit.config(text=translate[language_code]["ocr_captcha_force_submit"])
    lbl_ocr_captcha_image_source.config(text=translate[language_code]["ocr_captcha_image_source"])
    lbl_webdriver_type.config(text=translate[language_code]["webdriver_type"])
    lbl_chrome_extension.config(text=translate[language_code]["chrome_extension"])
    lbl_adjacent_seat.config(text=translate[language_code]["disable_adjacent_seat"])
    lbl_hide_some_image.config(text=translate[language_code]["hide_some_image"])
    lbl_block_facebook_network.config(text=translate[language_code]["block_facebook_network"])

    lbl_hide_some_image_recommand.config(text=translate[language_code]["recommand_enable"])
    lbl_block_facebook_network_recommand.config(text=translate[language_code]["recommand_enable"])

    lbl_auto_reload_page_interval.config(text=translate[language_code]["auto_reload_page_interval"])
    lbl_max_dwell_time.config(text=translate[language_code]["max_dwell_time"])
    lbl_cityline_queue_retry.config(text=translate[language_code]["cityline_queue_retry"])
    lbl_reset_browser_interval.config(text=translate[language_code]["reset_browser_interval"])
    lbl_proxy_server_port.config(text=translate[language_code]["proxy_server_port"])
    lbl_window_size.config(text=translate[language_code]["window_size"])

    lbl_headless.config(text=translate[language_code]["headless"])
    lbl_verbose.config(text=translate[language_code]["verbose"])

    lbl_remote_url.config(text=translate[language_code]["remote_url"])
    lbl_server_url.config(text=translate[language_code]["server_url"])
    lbl_online_dictionary_preview.config(text=translate[language_code]["preview"])
    lbl_auto_guess_options.config(text=translate[language_code]["auto_guess_options"])
    lbl_question.config(text=translate[language_code]["question"])
    lbl_answer.config(text=translate[language_code]["answer"])

    lbl_maxbot_status.config(text=translate[language_code]["running_status"])
    lbl_maxbot_last_url.config(text=translate[language_code]["running_url"])
    lbl_system_clock.config(text=translate[language_code]["system_clock"])
    lbl_idle_keyword.config(text=translate[language_code]["idle_keyword"])
    lbl_resume_keyword.config(text=translate[language_code]["resume_keyword"])
    lbl_idle_keyword_second.config(text=translate[language_code]["idle_keyword_second"])
    lbl_resume_keyword_second.config(text=translate[language_code]["resume_keyword_second"])

    chk_auto_press_next_step_button.config(text=translate[language_code]["enable"])
    chk_auto_fill_ticket_number.config(text=translate[language_code]["enable"])
    chk_date_auto_select.config(text=translate[language_code]["enable"])
    chk_area_auto_select.config(text=translate[language_code]["enable"])
    chk_pass_date_is_sold_out.config(text=translate[language_code]["enable"])
    chk_auto_reload_coming_soon_page.config(text=translate[language_code]["enable"])
    chk_play_ticket_sound.config(text=translate[language_code]["enable"])
    chk_play_order_sound.config(text=translate[language_code]["enable"])
    chk_ocr_captcha.config(text=translate[language_code]["enable"])
    chk_ocr_captcha_ddddocr_beta.config(text=translate[language_code]["enable"])
    chk_ocr_captcha_force_submit.config(text=translate[language_code]["enable"])
    chk_chrome_extension.config(text=translate[language_code]["enable"])
    chk_adjacent_seat.config(text=translate[language_code]["enable"])
    chk_hide_some_image.config(text=translate[language_code]["enable"])
    chk_block_facebook_network.config(text=translate[language_code]["enable"])

    chk_headless.config(text=translate[language_code]["enable"])
    chk_verbose.config(text=translate[language_code]["enable"])
    chk_auto_guess_options.config(text=translate[language_code]["enable"])
    chk_cityline_queue_retry.config(text=translate[language_code]["enable"])

    tabControl.tab(0, text=translate[language_code]["preference"])
    tabControl.tab(1, text=translate[language_code]["advanced"])
    tabControl.tab(2, text=translate[language_code]["verification_word"])
    tabControl.tab(3, text=translate[language_code]["maxbot_server"])
    tabControl.tab(4, text=translate[language_code]["autofill"])
    tabControl.tab(5, text=translate[language_code]["runtime"])
    tabControl.tab(6, text=translate[language_code]["about"])

    global lbl_tixcraft_sid
    global lbl_ibon_ibonqware
    global lbl_facebook_account
    global lbl_kktix_account
    global lbl_fami_account
    global lbl_cityline_account
    global lbl_urbtix_account
    global lbl_hkticketing_account
    global lbl_kham_account
    global lbl_ticket_account
    global lbl_udn_account
    global lbl_ticketplus_account

    global lbl_password
    global lbl_facebook_password
    global lbl_kktix_password
    global lbl_fami_password
    global lbl_cityline_password
    global lbl_urbtix_password
    global lbl_hkticketing_password
    global lbl_kham_password
    global lbl_ticket_password
    global lbl_udn_password
    global lbl_ticketplus_password

    global lbl_save_password_alert

    global lbl_play_ticket_sound
    global lbl_play_order_sound
    global lbl_play_sound_filename

    lbl_tixcraft_sid.config(text=translate[language_code]["tixcraft_sid"])
    lbl_ibon_ibonqware.config(text=translate[language_code]["ibon_ibonqware"])
    lbl_facebook_account.config(text=translate[language_code]["facebook_account"])
    lbl_kktix_account.config(text=translate[language_code]["kktix_account"])
    lbl_fami_account.config(text=translate[language_code]["fami_account"])
    lbl_cityline_account.config(text=translate[language_code]["cityline_account"])
    lbl_urbtix_account.config(text=translate[language_code]["urbtix_account"])
    lbl_hkticketing_account.config(text=translate[language_code]["hkticketing_account"])
    lbl_kham_account.config(text=translate[language_code]["kham_account"])
    lbl_ticket_account.config(text=translate[language_code]["ticket_account"])
    lbl_udn_account.config(text=translate[language_code]["udn_account"])
    lbl_ticketplus_account.config(text=translate[language_code]["ticketplus_account"])

    lbl_password.config(text=translate[language_code]["password"])
    # lbl_facebook_password.config(text=translate[language_code]["facebook_password"])
    # lbl_kktix_password.config(text=translate[language_code]["kktix_password"])
    # lbl_cityline_password.config(text=translate[language_code]["cityline_password"])
    # lbl_urbtix_password.config(text=translate[language_code]["urbtix_password"])
    # lbl_hkticketing_password.config(text=translate[language_code]["hkticketing_password"])
    # lbl_kham_password.config(text=translate[language_code]["kham_password"])
    # lbl_ticket_password.config(text=translate[language_code]["ticket_password"])
    # lbl_ticketplus_password.config(text=translate[language_code]["ticketplus_password"])

    lbl_save_password_alert.config(text=translate[language_code]["save_password_alert"])

    lbl_play_ticket_sound.config(text=translate[language_code]["play_ticket_sound"])
    lbl_play_order_sound.config(text=translate[language_code]["play_order_sound"])
    lbl_play_sound_filename.config(text=translate[language_code]["play_sound_filename"])

    lbl_slogan.config(text=translate[language_code]["maxbot_slogan"])
    lbl_help.config(text=translate[language_code]["help"])
    lbl_donate.config(text=translate[language_code]["donate"])
    lbl_release.config(text=translate[language_code]["release"])

    global btn_run
    global btn_save
    global btn_exit
    global btn_restore_defaults
    global btn_launcher

    global btn_idle
    global btn_resume

    btn_run.config(text=translate[language_code]["run"])
    btn_save.config(text=translate[language_code]["save"])
    if btn_exit:
        btn_exit.config(text=translate[language_code]["exit"])
    btn_restore_defaults.config(text=translate[language_code]["restore_defaults"])
    btn_launcher.config(text=translate[language_code]["config_launcher"])

    btn_idle.config(text=translate[language_code]["idle"])
    btn_resume.config(text=translate[language_code]["resume"])


def callbackHomepageOnChange(event):
    showHideBlocks()


def callbackDateAutoOnChange():
    showHideTixcraftBlocks()


def callbackAreaAutoOnChange():
    showHideAreaBlocks()


def showHideBlocks():
    global UI_PADDING_X

    global frame_group_kktix
    global frame_group_kktix_index
    global frame_group_tixcraft
    global frame_group_tixcraft_index

    global combo_homepage

    new_homepage = ""
    if 'combo_homepage' in globals():
        new_homepage = combo_homepage.get().strip()
        # print("new homepage value:", new_homepage)

    BLOCK_STYLE_TIXCRAFT = 0
    BLOCK_STYLE_KKTIX = 1
    STYLE_KKTIX_DOMAIN_LIST = ['kktix']

    global combo_webdriver_type
    if 'combo_webdriver_type' in globals():
        if 'cityline.com' in new_homepage:
            combo_webdriver_type.set("nodriver")

    show_block_index = BLOCK_STYLE_TIXCRAFT
    for domain_name in STYLE_KKTIX_DOMAIN_LIST:
        if domain_name in new_homepage:
            show_block_index = BLOCK_STYLE_KKTIX

    if 'frame_group_kktix' in globals():
        if show_block_index == BLOCK_STYLE_KKTIX:
            frame_group_kktix.grid(column=0, row=frame_group_kktix_index, padx=UI_PADDING_X)
            frame_group_tixcraft.grid_forget()
        else:
            frame_group_tixcraft.grid(column=0, row=frame_group_tixcraft_index, padx=UI_PADDING_X)
            frame_group_kktix.grid_forget()

        showHideTixcraftBlocks()


def showHideOcrCaptchaWithSubmit():
    global chk_state_ocr_captcha
    is_ocr_captcha_enable = bool(chk_state_ocr_captcha.get())

    global ocr_captcha_force_submit_index
    global lbl_ocr_captcha_force_submit
    global chk_ocr_captcha_force_submit

    global lbl_ocr_captcha_ddddocr_beta
    global chk_ocr_captcha_ddddocr_beta

    if is_ocr_captcha_enable:
        # show.
        lbl_ocr_captcha_force_submit.grid(column=0, row=ocr_captcha_force_submit_index, sticky=E)
        chk_ocr_captcha_force_submit.grid(column=1, row=ocr_captcha_force_submit_index, sticky=W)

        lbl_ocr_captcha_ddddocr_beta.grid(column=0, row=ocr_captcha_force_submit_index - 1, sticky=E)
        chk_ocr_captcha_ddddocr_beta.grid(column=1, row=ocr_captcha_force_submit_index - 1, sticky=W)
    else:
        # hide
        lbl_ocr_captcha_force_submit.grid_forget()
        chk_ocr_captcha_force_submit.grid_forget()

        lbl_ocr_captcha_ddddocr_beta.grid_forget()
        chk_ocr_captcha_ddddocr_beta.grid_forget()


# purpose: show detail blocks if master field is enable.
def showHideTixcraftBlocks():
    # for tixcraft show/hide enable.
    global chk_state_date_auto_select

    global date_auto_select_mode_index
    global lbl_date_auto_select_mode
    global combo_date_auto_select_mode

    global date_keyword_index
    global lbl_date_keyword
    global txt_date_keyword

    is_date_set_to_enable = bool(chk_state_date_auto_select.get())

    if is_date_set_to_enable:
        # show
        lbl_date_auto_select_mode.grid(column=0, row=date_auto_select_mode_index, sticky=E)
        combo_date_auto_select_mode.grid(column=1, row=date_auto_select_mode_index, sticky=W)

        lbl_date_keyword.grid(column=0, row=date_keyword_index, sticky=E + N)
        txt_date_keyword.grid(column=1, row=date_keyword_index, sticky=W)
    else:
        # hide
        lbl_date_auto_select_mode.grid_forget()
        combo_date_auto_select_mode.grid_forget()

        lbl_date_keyword.grid_forget()
        txt_date_keyword.grid_forget()


# purpose: show detail of area block.
def showHideAreaBlocks():
    # for tixcraft show/hide enable.
    global chk_state_area_auto_select

    global area_auto_select_mode_index
    global lbl_area_auto_select_mode
    global combo_area_auto_select_mode

    area_keyword_index = area_auto_select_mode_index + 1
    keyword_exclude_index = area_auto_select_mode_index + 2

    global lbl_area_keyword
    global txt_area_keyword

    global lbl_keyword_exclude
    global txt_keyword_exclude

    is_area_set_to_enable = bool(chk_state_area_auto_select.get())

    if is_area_set_to_enable:
        # show
        lbl_area_auto_select_mode.grid(column=0, row=area_auto_select_mode_index, sticky=E)
        combo_area_auto_select_mode.grid(column=1, row=area_auto_select_mode_index, sticky=W)

        lbl_area_keyword.grid(column=0, row=area_keyword_index, sticky=E + N)
        txt_area_keyword.grid(column=1, row=area_keyword_index, sticky=W)

        lbl_keyword_exclude.grid(column=0, row=keyword_exclude_index, sticky=E + N)
        txt_keyword_exclude.grid(column=1, row=keyword_exclude_index, sticky=W)

    else:
        # hide
        lbl_area_auto_select_mode.grid_forget()
        combo_area_auto_select_mode.grid_forget()

        lbl_area_keyword.grid_forget()
        txt_area_keyword.grid_forget()

        lbl_keyword_exclude.grid_forget()
        txt_keyword_exclude.grid_forget()


def on_homepage_configure(event):
    font = tkfont.nametofont(str(event.widget.cget('font')))
    width = font.measure(CONST_SUPPORTED_SITES[len(CONST_SUPPORTED_SITES) - 1] + "0") - event.width
    style = ttk.Style()
    style.configure('TCombobox', postoffset=(0, 0, width, 0))


def PreferenctTab(root, config_dict, language_code, UI_PADDING_X):
    # output config:
    print("setting app version:", CONST_APP_VERSION)
    print("python version:", platform.python_version())
    print("platform:", platform.platform())

    global lbl_kktix
    global lbl_tixcraft

    row_count = 0

    frame_group_header = Frame(root)
    group_row_count = 0

    # first row need padding Y
    global lbl_homepage
    lbl_homepage = Label(frame_group_header, text=translate[language_code]['homepage'])
    lbl_homepage.grid(column=0, row=group_row_count, sticky=E)

    global combo_homepage
    combo_homepage = ttk.Combobox(frame_group_header, width=30)
    combo_homepage['values'] = CONST_SUPPORTED_SITES
    combo_homepage.set(config_dict["homepage"])
    combo_homepage.bind("<<ComboboxSelected>>", callbackHomepageOnChange)
    # combo_homepage.bind('<Configure>', on_homepage_configure)
    combo_homepage.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_ticket_number
    lbl_ticket_number = Label(frame_group_header, text=translate[language_code]['ticket_number'])
    lbl_ticket_number.grid(column=0, row=group_row_count, sticky=E)

    global combo_ticket_number
    # for text format.
    # PS: some user keyin wrong type. @_@;
    '''
    global combo_ticket_number_value
    combo_ticket_number_value = StringVar(frame_group_header, value=ticket_number)
    combo_ticket_number = Entry(frame_group_header, width=30, textvariable = combo_ticket_number_value)
    combo_ticket_number.grid(column=1, row=group_row_count, sticky = W)
    '''
    combo_ticket_number = ttk.Combobox(frame_group_header, state="readonly", width=30)
    combo_ticket_number['values'] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
    # combo_ticket_number.current(0)
    combo_ticket_number.set(str(config_dict["ticket_number"]))
    combo_ticket_number.grid(column=1, row=group_row_count, sticky=W)

    frame_group_header.grid(column=0, row=row_count, sticky=W, padx=UI_PADDING_X)

    group_row_count += 1

    global lbl_refresh_datetime
    lbl_refresh_datetime = Label(frame_group_header, text=translate[language_code]['refresh_datetime'])
    lbl_refresh_datetime.grid(column=0, row=group_row_count, sticky=E)

    global txt_refresh_datetime
    txt_refresh_datetime_value = StringVar(frame_group_header, value=str(config_dict["refresh_datetime"]))
    txt_refresh_datetime = Entry(frame_group_header, width=30, textvariable=txt_refresh_datetime_value)
    txt_refresh_datetime.grid(column=1, row=group_row_count, sticky=W)

    row_count += 1

    # for sub group KKTix.
    global frame_group_kktix
    frame_group_kktix = Frame(root)
    group_row_count = 0

    # start sub group...
    group_row_count += 1

    global lbl_auto_press_next_step_button
    lbl_auto_press_next_step_button = Label(frame_group_kktix,
                                            text=translate[language_code]['auto_press_next_step_button'])
    lbl_auto_press_next_step_button.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_auto_press_next_step_button
    chk_state_auto_press_next_step_button = BooleanVar()
    chk_state_auto_press_next_step_button.set(config_dict["kktix"]["auto_press_next_step_button"])

    global chk_auto_press_next_step_button
    chk_auto_press_next_step_button = Checkbutton(frame_group_kktix, text=translate[language_code]['enable'],
                                                  variable=chk_state_auto_press_next_step_button)
    chk_auto_press_next_step_button.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_auto_fill_ticket_number
    lbl_auto_fill_ticket_number = Label(frame_group_kktix, text=translate[language_code]['auto_fill_ticket_number'])
    lbl_auto_fill_ticket_number.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_auto_fill_ticket_number
    chk_state_auto_fill_ticket_number = BooleanVar()
    chk_state_auto_fill_ticket_number.set(config_dict["kktix"]["auto_fill_ticket_number"])

    global chk_auto_fill_ticket_number
    chk_auto_fill_ticket_number = Checkbutton(frame_group_kktix, text=translate[language_code]['enable'],
                                              variable=chk_state_auto_fill_ticket_number)
    chk_auto_fill_ticket_number.grid(column=1, row=group_row_count, sticky=W)

    global frame_group_kktix_index
    frame_group_kktix_index = row_count
    # PS: don't need show when onload(), because show/hide block will load again.
    # frame_group_kktix.grid(column=0, row=row_count, sticky = W, padx=UI_PADDING_X)

    row_count += 1

    # for sub group tixcraft.
    global frame_group_tixcraft
    frame_group_tixcraft = Frame(root)
    group_row_count = 0

    # start sub group.
    group_row_count += 1

    global lbl_date_auto_select
    lbl_date_auto_select = Label(frame_group_tixcraft, text=translate[language_code]['date_auto_select'])
    lbl_date_auto_select.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_date_auto_select
    chk_state_date_auto_select = BooleanVar()
    chk_state_date_auto_select.set(config_dict["date_auto_select"]["enable"])

    global chk_date_auto_select
    chk_date_auto_select = Checkbutton(frame_group_tixcraft, text=translate[language_code]['enable'],
                                       variable=chk_state_date_auto_select, command=callbackDateAutoOnChange)
    chk_date_auto_select.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global date_auto_select_mode_index
    date_auto_select_mode_index = group_row_count

    global lbl_date_auto_select_mode
    lbl_date_auto_select_mode = Label(frame_group_tixcraft, text=translate[language_code]['date_select_order'])
    lbl_date_auto_select_mode.grid(column=0, row=date_auto_select_mode_index, sticky=E)

    global combo_date_auto_select_mode
    combo_date_auto_select_mode = ttk.Combobox(frame_group_tixcraft, state="readonly", width=30)
    combo_date_auto_select_mode['values'] = CONST_SELECT_OPTIONS_DEFAULT
    combo_date_auto_select_mode.set(config_dict["date_auto_select"]["mode"])
    combo_date_auto_select_mode.grid(column=1, row=date_auto_select_mode_index, sticky=W)

    group_row_count += 1

    global date_keyword_index
    date_keyword_index = group_row_count

    global lbl_date_keyword
    lbl_date_keyword = Label(frame_group_tixcraft, text=translate[language_code]['date_keyword'])
    lbl_date_keyword.grid(column=0, row=date_keyword_index, sticky=E + N)

    global txt_date_keyword
    txt_date_keyword = Text(frame_group_tixcraft, width=30, height=4)
    txt_date_keyword.grid(column=1, row=group_row_count, sticky=W)
    txt_date_keyword.insert("1.0", config_dict["date_auto_select"]["date_keyword"].strip())

    group_row_count += 1

    global lbl_pass_date_is_sold_out
    lbl_pass_date_is_sold_out = Label(frame_group_tixcraft, text=translate[language_code]['pass_date_is_sold_out'])
    lbl_pass_date_is_sold_out.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_pass_date_is_sold_out
    chk_state_pass_date_is_sold_out = BooleanVar()
    chk_state_pass_date_is_sold_out.set(config_dict["tixcraft"]["pass_date_is_sold_out"])

    global chk_pass_date_is_sold_out
    chk_pass_date_is_sold_out = Checkbutton(frame_group_tixcraft, text=translate[language_code]['enable'],
                                            variable=chk_state_pass_date_is_sold_out)
    chk_pass_date_is_sold_out.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_auto_reload_coming_soon_page
    lbl_auto_reload_coming_soon_page = Label(frame_group_tixcraft,
                                             text=translate[language_code]['auto_reload_coming_soon_page'])
    lbl_auto_reload_coming_soon_page.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_auto_reload_coming_soon_page
    chk_state_auto_reload_coming_soon_page = BooleanVar()
    chk_state_auto_reload_coming_soon_page.set(config_dict["tixcraft"]["auto_reload_coming_soon_page"])

    global chk_auto_reload_coming_soon_page
    chk_auto_reload_coming_soon_page = Checkbutton(frame_group_tixcraft, text=translate[language_code]['enable'],
                                                   variable=chk_state_auto_reload_coming_soon_page)
    chk_auto_reload_coming_soon_page.grid(column=1, row=group_row_count, sticky=W)

    # final flush.
    global frame_group_tixcraft_index
    frame_group_tixcraft_index = row_count
    # PS: don't need show when onload(), because show/hide block will load again.
    # frame_group_tixcraft.grid(column=0, row=row_count, sticky = W, padx=UI_PADDING_X)

    row_count += 1

    showHideBlocks()

    # for area block.
    global frame_group_area
    frame_group_area = Frame(root)
    group_row_count = 0

    global lbl_area_auto_select
    lbl_area_auto_select = Label(frame_group_area, text=translate[language_code]['area_auto_select'])
    lbl_area_auto_select.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_area_auto_select
    chk_state_area_auto_select = BooleanVar()
    chk_state_area_auto_select.set(config_dict["area_auto_select"]["enable"])

    global chk_area_auto_select
    chk_area_auto_select = Checkbutton(frame_group_area, text=translate[language_code]['enable'],
                                       variable=chk_state_area_auto_select, command=callbackAreaAutoOnChange)
    chk_area_auto_select.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global area_auto_select_mode_index
    area_auto_select_mode_index = group_row_count

    global lbl_area_auto_select_mode
    lbl_area_auto_select_mode = Label(frame_group_area, text=translate[language_code]['area_auto_select'])
    lbl_area_auto_select_mode.grid(column=0, row=area_auto_select_mode_index, sticky=E)

    global combo_area_auto_select_mode
    combo_area_auto_select_mode = ttk.Combobox(frame_group_area, state="readonly", width=30)
    combo_area_auto_select_mode['values'] = CONST_SELECT_OPTIONS_DEFAULT
    combo_area_auto_select_mode.set(config_dict["area_auto_select"]["mode"])
    combo_area_auto_select_mode.grid(column=1, row=area_auto_select_mode_index, sticky=W)

    group_row_count += 1

    global lbl_area_keyword
    lbl_area_keyword = Label(frame_group_area, text=translate[language_code]['area_keyword'])
    lbl_area_keyword.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_area_keyword
    txt_area_keyword = Text(frame_group_area, width=30, height=4)
    txt_area_keyword.grid(column=1, row=group_row_count, sticky=W)
    txt_area_keyword.insert("1.0", config_dict["area_auto_select"]["area_keyword"].strip())

    group_row_count += 1

    global lbl_keyword_exclude
    lbl_keyword_exclude = Label(frame_group_area, text=translate[language_code]['keyword_exclude'])
    lbl_keyword_exclude.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_keyword_exclude
    txt_keyword_exclude = Text(frame_group_area, width=30, height=4)
    txt_keyword_exclude.grid(column=1, row=group_row_count, sticky=W)
    txt_keyword_exclude.insert("1.0", config_dict["keyword_exclude"].strip())

    group_row_count += 1

    global lbl_keyword_usage
    lbl_keyword_usage = Label(frame_group_area, text=translate[language_code]['keyword_usage'])
    lbl_keyword_usage.grid(column=1, row=group_row_count, sticky=W)

    # flush
    frame_group_area.grid(column=0, row=row_count, sticky=W, padx=UI_PADDING_X)

    showHideAreaBlocks()


def AdvancedTab(root, config_dict, language_code, UI_PADDING_X):
    browser_options = ("chrome", "firefox", "edge", "safari", "brave")
    webdriver_type_options = (CONST_WEBDRIVER_TYPE_SELENIUM, CONST_WEBDRIVER_TYPE_UC)

    not_support_python_version = ["3.6.", "3.7.", "3.8."]
    is_current_version_after_3_9 = True
    for not_support_ver in not_support_python_version:
        current_version = platform.python_version()
        if current_version[:4] == not_support_ver:
            is_current_version_after_3_9 = False
            break
    if is_current_version_after_3_9:
        webdriver_type_options = (CONST_WEBDRIVER_TYPE_SELENIUM, CONST_WEBDRIVER_TYPE_UC, CONST_WEBDRIVER_TYPE_NODRIVER)
        pass

    row_count = 0

    frame_group_header = Frame(root)
    group_row_count = 0

    # assign default value.
    play_sound_filename = config_dict["advanced"]["play_sound"]["filename"].strip()
    if play_sound_filename is None:
        play_sound_filename = ""
    if len(play_sound_filename) == 0:
        play_sound_filename = play_sound_filename_default

    global lbl_browser
    lbl_browser = Label(frame_group_header, text=translate[language_code]['browser'])
    lbl_browser.grid(column=0, row=group_row_count, sticky=E)

    global combo_browser
    combo_browser = ttk.Combobox(frame_group_header, state="readonly", width=30)
    combo_browser['values'] = browser_options
    combo_browser.set(config_dict['browser'])
    combo_browser.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_language
    lbl_language = Label(frame_group_header, text=translate[language_code]['language'])
    lbl_language.grid(column=0, row=group_row_count, sticky=E)

    global combo_language
    combo_language = ttk.Combobox(frame_group_header, state="readonly", width=30)
    combo_language['values'] = ("English", "繁體中文", "簡体中文", "日本語")
    combo_language.set(config_dict['language'])
    combo_language.bind("<<ComboboxSelected>>", callbackLanguageOnChange)
    combo_language.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_ocr_captcha_image_source
    lbl_ocr_captcha_image_source = Label(frame_group_header, text=translate[language_code]['ocr_captcha_image_source'])
    lbl_ocr_captcha_image_source.grid(column=0, row=group_row_count, sticky=E)

    global combo_ocr_captcha_image_source
    combo_ocr_captcha_image_source = ttk.Combobox(frame_group_header, state="readonly", width=30)
    combo_ocr_captcha_image_source['values'] = (
        CONST_OCR_CAPTCH_IMAGE_SOURCE_NON_BROWSER, CONST_OCR_CAPTCH_IMAGE_SOURCE_CANVAS)
    combo_ocr_captcha_image_source.set(config_dict["ocr_captcha"]["image_source"])
    combo_ocr_captcha_image_source.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_webdriver_type
    lbl_webdriver_type = Label(frame_group_header, text=translate[language_code]['webdriver_type'])
    lbl_webdriver_type.grid(column=0, row=group_row_count, sticky=E)

    global combo_webdriver_type
    combo_webdriver_type = ttk.Combobox(frame_group_header, state="readonly", width=30)
    combo_webdriver_type['values'] = webdriver_type_options
    combo_webdriver_type.set(config_dict["webdriver_type"])
    combo_webdriver_type.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_play_ticket_sound
    lbl_play_ticket_sound = Label(frame_group_header, text=translate[language_code]['play_ticket_sound'])
    lbl_play_ticket_sound.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_play_ticket_sound
    chk_state_play_ticket_sound = BooleanVar()
    chk_state_play_ticket_sound.set(config_dict["advanced"]["play_sound"]["ticket"])

    global chk_play_ticket_sound
    chk_play_ticket_sound = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                        variable=chk_state_play_ticket_sound)
    chk_play_ticket_sound.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_play_order_sound
    lbl_play_order_sound = Label(frame_group_header, text=translate[language_code]['play_order_sound'])
    lbl_play_order_sound.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_play_order_sound
    chk_state_play_order_sound = BooleanVar()
    chk_state_play_order_sound.set(config_dict["advanced"]["play_sound"]["order"])

    global chk_play_order_sound
    chk_play_order_sound = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                       variable=chk_state_play_order_sound)
    chk_play_order_sound.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_play_sound_filename
    lbl_play_sound_filename = Label(frame_group_header, text=translate[language_code]['play_sound_filename'])
    lbl_play_sound_filename.grid(column=0, row=group_row_count, sticky=E)

    global txt_play_sound_filename
    txt_play_sound_filename_value = StringVar(frame_group_header, value=play_sound_filename)
    txt_play_sound_filename = Entry(frame_group_header, width=30, textvariable=txt_play_sound_filename_value)
    txt_play_sound_filename.grid(column=1, row=group_row_count, sticky=W)

    icon_play_filename = "icon_play_1.gif"
    icon_play_img = PhotoImage(file=icon_play_filename)

    lbl_icon_play = Label(frame_group_header, image=icon_play_img, cursor="hand2")
    lbl_icon_play.image = icon_play_img
    lbl_icon_play.grid(column=2, row=group_row_count, sticky=W)
    lbl_icon_play.bind("<Button-1>", lambda e: btn_preview_sound_clicked())

    group_row_count += 1

    global lbl_auto_reload_page_interval
    lbl_auto_reload_page_interval = Label(frame_group_header,
                                          text=translate[language_code]['auto_reload_page_interval'])
    lbl_auto_reload_page_interval.grid(column=0, row=group_row_count, sticky=E)

    global txt_auto_reload_page_interval
    txt_auto_reload_page_interval_value = StringVar(frame_group_header,
                                                    value=config_dict["advanced"]["auto_reload_page_interval"])
    txt_auto_reload_page_interval = Entry(frame_group_header, width=30,
                                          textvariable=txt_auto_reload_page_interval_value)
    txt_auto_reload_page_interval.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_max_dwell_time
    lbl_max_dwell_time = Label(frame_group_header, text=translate[language_code]['max_dwell_time'])
    lbl_max_dwell_time.grid(column=0, row=group_row_count, sticky=E)

    global txt_max_dwell_time
    txt_max_dwell_time_value = StringVar(frame_group_header, value=config_dict["kktix"]["max_dwell_time"])
    txt_max_dwell_time = Entry(frame_group_header, width=30, textvariable=txt_max_dwell_time_value)
    txt_max_dwell_time.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_cityline_queue_retry
    lbl_cityline_queue_retry = Label(frame_group_header, text=translate[language_code]['cityline_queue_retry'])
    lbl_cityline_queue_retry.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_cityline_queue_retry
    chk_state_cityline_queue_retry = BooleanVar()
    chk_state_cityline_queue_retry.set(config_dict["cityline"]["cityline_queue_retry"])

    global chk_cityline_queue_retry
    chk_cityline_queue_retry = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                           variable=chk_state_cityline_queue_retry)
    chk_cityline_queue_retry.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_reset_browser_interval
    lbl_reset_browser_interval = Label(frame_group_header, text=translate[language_code]['reset_browser_interval'])
    lbl_reset_browser_interval.grid(column=0, row=group_row_count, sticky=E)

    global txt_reset_browser_interval
    txt_reset_browser_interval_value = StringVar(frame_group_header,
                                                 value=config_dict["advanced"]["reset_browser_interval"])
    txt_reset_browser_interval = Entry(frame_group_header, width=30, textvariable=txt_reset_browser_interval_value)
    txt_reset_browser_interval.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_proxy_server_port
    lbl_proxy_server_port = Label(frame_group_header, text=translate[language_code]['proxy_server_port'])
    lbl_proxy_server_port.grid(column=0, row=group_row_count, sticky=E)

    global txt_proxy_server_port
    txt_proxy_server_port_value = StringVar(frame_group_header, value=config_dict["advanced"]["proxy_server_port"])
    txt_proxy_server_port = Entry(frame_group_header, width=30, textvariable=txt_proxy_server_port_value)
    txt_proxy_server_port.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_window_size
    lbl_window_size = Label(frame_group_header, text=translate[language_code]['window_size'])
    lbl_window_size.grid(column=0, row=group_row_count, sticky=E)

    global txt_window_size
    txt_window_size_value = StringVar(frame_group_header, value=config_dict["advanced"]["window_size"])
    txt_window_size = Entry(frame_group_header, width=30, textvariable=txt_window_size_value)
    txt_window_size.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_chrome_extension
    lbl_chrome_extension = Label(frame_group_header, text=translate[language_code]['chrome_extension'])
    lbl_chrome_extension.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_chrome_extension
    chk_state_chrome_extension = BooleanVar()
    chk_state_chrome_extension.set(config_dict["advanced"]["chrome_extension"])

    global chk_chrome_extension
    chk_chrome_extension = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                       variable=chk_state_chrome_extension)
    chk_chrome_extension.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_adjacent_seat
    lbl_adjacent_seat = Label(frame_group_header, text=translate[language_code]['disable_adjacent_seat'])
    lbl_adjacent_seat.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_adjacent_seat
    chk_state_adjacent_seat = BooleanVar()
    chk_state_adjacent_seat.set(config_dict["advanced"]["disable_adjacent_seat"])

    global chk_adjacent_seat
    chk_adjacent_seat = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                    variable=chk_state_adjacent_seat)
    chk_adjacent_seat.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_hide_some_image
    lbl_hide_some_image = Label(frame_group_header, text=translate[language_code]['hide_some_image'])
    lbl_hide_some_image.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_hide_some_image
    chk_state_hide_some_image = BooleanVar()
    chk_state_hide_some_image.set(config_dict["advanced"]["hide_some_image"])

    global chk_hide_some_image
    chk_hide_some_image = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                      variable=chk_state_hide_some_image)
    chk_hide_some_image.grid(column=1, row=group_row_count, sticky=W)

    global lbl_hide_some_image_recommand
    lbl_hide_some_image_recommand = Label(frame_group_header, text=translate[language_code]['recommand_enable'])
    lbl_hide_some_image_recommand.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_block_facebook_network
    lbl_block_facebook_network = Label(frame_group_header, text=translate[language_code]['block_facebook_network'])
    lbl_block_facebook_network.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_block_facebook_network
    chk_state_block_facebook_network = BooleanVar()
    chk_state_block_facebook_network.set(config_dict["advanced"]["block_facebook_network"])

    global chk_block_facebook_network
    chk_block_facebook_network = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                             variable=chk_state_block_facebook_network)
    chk_block_facebook_network.grid(column=1, row=group_row_count, sticky=W)

    global lbl_block_facebook_network_recommand
    lbl_block_facebook_network_recommand = Label(frame_group_header, text=translate[language_code]['recommand_enable'])
    lbl_block_facebook_network_recommand.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_headless
    lbl_headless = Label(frame_group_header, text=translate[language_code]['headless'])
    lbl_headless.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_headless
    chk_state_headless = BooleanVar()
    chk_state_headless.set(config_dict['advanced']["headless"])

    global chk_headless
    chk_headless = Checkbutton(frame_group_header, text=translate[language_code]['enable'], variable=chk_state_headless)
    chk_headless.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_verbose
    lbl_verbose = Label(frame_group_header, text=translate[language_code]['verbose'])
    # maybe enable in future.
    # lbl_verbose.grid(column=0, row=group_row_count, sticky = E)

    global chk_state_verbose
    chk_state_verbose = BooleanVar()
    chk_state_verbose.set(config_dict['advanced']["verbose"])

    global chk_verbose
    chk_verbose = Checkbutton(frame_group_header, text=translate[language_code]['enable'], variable=chk_state_verbose)
    # maybe enable in future.
    # chk_verbose.grid(column=1, row=group_row_count, sticky = W)

    group_row_count += 1

    global lbl_ocr_captcha
    lbl_ocr_captcha = Label(frame_group_header, text=translate[language_code]["ocr_captcha"])
    lbl_ocr_captcha.grid(column=0, row=group_row_count, sticky=E)

    frame_group_ddddocr_enable = Frame(frame_group_header)

    global chk_state_ocr_captcha
    chk_state_ocr_captcha = BooleanVar()
    chk_state_ocr_captcha.set(config_dict["ocr_captcha"]["enable"])

    global chk_ocr_captcha
    chk_ocr_captcha = Checkbutton(frame_group_ddddocr_enable, text=translate[language_code]['enable'],
                                  variable=chk_state_ocr_captcha, command=showHideOcrCaptchaWithSubmit)
    chk_ocr_captcha.grid(column=0, row=0, sticky=W)

    frame_group_ddddocr_enable.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_ocr_captcha_ddddocr_beta
    lbl_ocr_captcha_ddddocr_beta = Label(frame_group_header, text=translate[language_code]['ocr_captcha_ddddocr_beta'])
    lbl_ocr_captcha_ddddocr_beta.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_ocr_captcha_ddddocr_beta
    chk_state_ocr_captcha_ddddocr_beta = BooleanVar()
    chk_state_ocr_captcha_ddddocr_beta.set(config_dict["ocr_captcha"]["beta"])

    global chk_ocr_captcha_ddddocr_beta
    chk_ocr_captcha_ddddocr_beta = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                               variable=chk_state_ocr_captcha_ddddocr_beta)
    chk_ocr_captcha_ddddocr_beta.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global ocr_captcha_force_submit_index
    ocr_captcha_force_submit_index = group_row_count

    global lbl_ocr_captcha_force_submit
    lbl_ocr_captcha_force_submit = Label(frame_group_header, text=translate[language_code]['ocr_captcha_force_submit'])
    lbl_ocr_captcha_force_submit.grid(column=0, row=ocr_captcha_force_submit_index, sticky=E)

    global chk_state_ocr_captcha_force_submit
    chk_state_ocr_captcha_force_submit = BooleanVar()
    chk_state_ocr_captcha_force_submit.set(config_dict["ocr_captcha"]["force_submit"])

    global chk_ocr_captcha_force_submit
    chk_ocr_captcha_force_submit = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                               variable=chk_state_ocr_captcha_force_submit)
    chk_ocr_captcha_force_submit.grid(column=1, row=group_row_count, sticky=W)

    frame_group_header.grid(column=0, row=row_count, padx=UI_PADDING_X)

    showHideOcrCaptchaWithSubmit()


def VerificationTab(root, config_dict, language_code, UI_PADDING_X):
    row_count = 0

    frame_group_header = Frame(root)
    group_row_count = 0

    global lbl_user_guess_string_description
    lbl_user_guess_string_description = Label(frame_group_header, text=translate[language_code]['user_guess_string'])
    lbl_user_guess_string_description.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_user_guess_string
    lbl_user_guess_string = Label(frame_group_header, text=translate[language_code]['local_dictionary'])
    lbl_user_guess_string.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_user_guess_string
    txt_user_guess_string = Text(frame_group_header, width=30, height=4)
    txt_user_guess_string.grid(column=1, row=group_row_count, sticky=W)
    txt_user_guess_string.insert("1.0", config_dict["advanced"]["user_guess_string"].strip())

    group_row_count += 1

    global lbl_remote_url
    lbl_remote_url = Label(frame_group_header, text=translate[language_code]['remote_url'])
    lbl_remote_url.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_remote_url
    txt_remote_url = Text(frame_group_header, width=30, height=4)
    txt_remote_url.grid(column=1, row=group_row_count, sticky=W)
    txt_remote_url.insert("1.0", config_dict['advanced']["remote_url"].strip())

    icon_preview_text_filename = "icon_chrome_4.gif"
    icon_preview_text_img = PhotoImage(file=icon_preview_text_filename)

    lbl_icon_preview_text = Label(frame_group_header, image=icon_preview_text_img, cursor="hand2")
    lbl_icon_preview_text.image = icon_preview_text_img
    lbl_icon_preview_text.grid(column=2, row=group_row_count, sticky=W + N)
    lbl_icon_preview_text.bind("<Button-1>", lambda e: btn_open_text_server_clicked())

    group_row_count += 1

    global lbl_online_dictionary_preview
    lbl_online_dictionary_preview = Label(frame_group_header, text=translate[language_code]['preview'])
    lbl_online_dictionary_preview.grid(column=0, row=group_row_count, sticky=E)

    global lbl_online_dictionary_preview_data
    lbl_online_dictionary_preview_data = Label(frame_group_header, text="")
    lbl_online_dictionary_preview_data.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_auto_guess_options
    lbl_auto_guess_options = Label(frame_group_header, text=translate[language_code]['auto_guess_options'])
    lbl_auto_guess_options.grid(column=0, row=group_row_count, sticky=E)

    global chk_state_auto_guess_options
    chk_state_auto_guess_options = BooleanVar()
    chk_state_auto_guess_options.set(config_dict["advanced"]["auto_guess_options"])

    global chk_auto_guess_options
    chk_auto_guess_options = Checkbutton(frame_group_header, text=translate[language_code]['enable'],
                                         variable=chk_state_auto_guess_options)
    chk_auto_guess_options.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    frame_group_header.grid(column=0, row=row_count, padx=UI_PADDING_X)


def ServerTab(root, config_dict, language_code, UI_PADDING_X):
    row_count = 0

    frame_group_header = Frame(root)
    group_row_count = 0

    global lbl_server_url
    lbl_server_url = Label(frame_group_header, text=translate[language_code]['server_url'])
    lbl_server_url.grid(column=0, row=group_row_count, sticky=E)

    local_ip = util.get_ip_address()
    ip_address = "http://%s:%d/" % (local_ip, CONST_SERVER_PORT)
    global lbl_ip_address
    lbl_ip_address = Label(frame_group_header, text=ip_address)
    lbl_ip_address.grid(column=1, row=group_row_count, sticky=W)

    icon_copy_filename = "icon_copy_2.gif"
    icon_copy_img = PhotoImage(file=icon_copy_filename)

    lbl_icon_copy_ip = Label(frame_group_header, image=icon_copy_img, cursor="hand2")
    lbl_icon_copy_ip.image = icon_copy_img
    lbl_icon_copy_ip.grid(column=2, row=group_row_count, sticky=W + N)
    lbl_icon_copy_ip.bind("<Button-1>", lambda e: btn_copy_ip_clicked())

    group_row_count += 1

    global lbl_question
    lbl_question = Label(frame_group_header, text=translate[language_code]['question'])
    lbl_question.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_question
    txt_question = Text(frame_group_header, width=50, height=22)
    txt_question.grid(column=1, row=group_row_count, sticky=W)
    txt_question.insert("1.0", "")

    lbl_icon_copy_question = Label(frame_group_header, image=icon_copy_img, cursor="hand2")
    lbl_icon_copy_question.image = icon_copy_img
    # lbl_icon_copy_question.grid(column=2, row=group_row_count, sticky = W+N)
    lbl_icon_copy_question.bind("<Button-1>", lambda e: btn_copy_question_clicked())

    icon_query_filename = "icon_query_5.gif"
    icon_query_img = PhotoImage(file=icon_query_filename)

    lbl_icon_query_question = Label(frame_group_header, image=icon_query_img, cursor="hand2")
    lbl_icon_query_question.image = icon_query_img
    lbl_icon_query_question.grid(column=2, row=group_row_count, sticky=W + N)
    lbl_icon_query_question.bind("<Button-1>", lambda e: btn_query_question_clicked())

    group_row_count += 1

    global lbl_answer
    lbl_answer = Label(frame_group_header, text=translate[language_code]['answer'])
    lbl_answer.grid(column=0, row=group_row_count, sticky=E)

    global txt_answer
    global txt_answer_value
    txt_answer_value = StringVar(frame_group_header, value="")
    txt_answer = Entry(frame_group_header, width=30, textvariable=txt_answer_value)
    txt_answer.grid(column=1, row=group_row_count, sticky=W)
    txt_answer.bind('<Control-v>', lambda e: btn_paste_answer_by_user())

    frame_group_header.grid(column=0, row=row_count, padx=UI_PADDING_X, pady=15)


def AutofillTab(root, config_dict, language_code, UI_PADDING_X):
    row_count = 0

    frame_group_header = Frame(root)
    group_row_count = 0

    global lbl_tixcraft_sid
    lbl_tixcraft_sid = Label(frame_group_header, text=translate[language_code]['tixcraft_sid'])
    lbl_tixcraft_sid.grid(column=0, row=group_row_count, sticky=E)

    global txt_tixcraft_sid
    txt_tixcraft_sid_value = StringVar(frame_group_header, value=config_dict["advanced"]["tixcraft_sid"].strip())
    txt_tixcraft_sid = Entry(frame_group_header, width=30, textvariable=txt_tixcraft_sid_value, show="*")
    txt_tixcraft_sid.grid(column=1, row=group_row_count, columnspan=2, sticky=W)

    group_row_count += 1

    global lbl_ibon_ibonqware
    lbl_ibon_ibonqware = Label(frame_group_header, text=translate[language_code]['ibon_ibonqware'])
    lbl_ibon_ibonqware.grid(column=0, row=group_row_count, sticky=E)

    global txt_ibon_ibonqware
    txt_ibon_ibonqware_value = StringVar(frame_group_header, value=config_dict["advanced"]["ibonqware"].strip())
    txt_ibon_ibonqware = Entry(frame_group_header, width=30, textvariable=txt_ibon_ibonqware_value, show="*")
    txt_ibon_ibonqware.grid(column=1, row=group_row_count, columnspan=2, sticky=W)

    group_row_count += 1

    global lbl_password
    lbl_password = Label(frame_group_header, text=translate[language_code]['password'])
    lbl_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_facebook_account
    lbl_facebook_account = Label(frame_group_header, text=translate[language_code]['facebook_account'])
    lbl_facebook_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_facebook_account
    txt_facebook_account_value = StringVar(frame_group_header,
                                           value=config_dict["advanced"]["facebook_account"].strip())
    txt_facebook_account = Entry(frame_group_header, width=15, textvariable=txt_facebook_account_value)
    txt_facebook_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_facebook_password
    txt_facebook_password_value = StringVar(frame_group_header,
                                            value=util.decryptMe(config_dict["advanced"]["facebook_password"].strip()))
    txt_facebook_password = Entry(frame_group_header, width=15, textvariable=txt_facebook_password_value, show="*")
    txt_facebook_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_kktix_account
    lbl_kktix_account = Label(frame_group_header, text=translate[language_code]['kktix_account'])
    lbl_kktix_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_kktix_account
    txt_kktix_account_value = StringVar(frame_group_header, value=config_dict["advanced"]["kktix_account"].strip())
    txt_kktix_account = Entry(frame_group_header, width=15, textvariable=txt_kktix_account_value)
    txt_kktix_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_kktix_password
    txt_kktix_password_value = StringVar(frame_group_header,
                                         value=util.decryptMe(config_dict["advanced"]["kktix_password"].strip()))
    txt_kktix_password = Entry(frame_group_header, width=15, textvariable=txt_kktix_password_value, show="*")
    txt_kktix_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_fami_account
    lbl_fami_account = Label(frame_group_header, text=translate[language_code]['fami_account'])
    lbl_fami_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_fami_account
    txt_fami_account_value = StringVar(frame_group_header, value=config_dict["advanced"]["fami_account"].strip())
    txt_fami_account = Entry(frame_group_header, width=15, textvariable=txt_fami_account_value)
    txt_fami_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_fami_password
    txt_fami_password_value = StringVar(frame_group_header,
                                        value=util.decryptMe(config_dict["advanced"]["fami_password"].strip()))
    txt_fami_password = Entry(frame_group_header, width=15, textvariable=txt_fami_password_value, show="*")
    txt_fami_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_cityline_account
    lbl_cityline_account = Label(frame_group_header, text=translate[language_code]['cityline_account'])
    lbl_cityline_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_cityline_account
    txt_cityline_account_value = StringVar(frame_group_header,
                                           value=config_dict["advanced"]["cityline_account"].strip())
    txt_cityline_account = Entry(frame_group_header, width=30, textvariable=txt_cityline_account_value)
    txt_cityline_account.grid(column=1, row=group_row_count, sticky=W, columnspan=2)

    global txt_cityline_password
    txt_cityline_password_value = StringVar(frame_group_header,
                                            value=util.decryptMe(config_dict["advanced"]["cityline_password"].strip()))
    txt_cityline_password = Entry(frame_group_header, width=15, textvariable=txt_cityline_password_value, show="*")
    # txt_cityline_password.grid(column=2, row=group_row_count, sticky = W)

    group_row_count += 1

    global lbl_urbtix_account
    lbl_urbtix_account = Label(frame_group_header, text=translate[language_code]['urbtix_account'])
    lbl_urbtix_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_urbtix_account
    txt_urbtix_account_value = StringVar(frame_group_header, value=config_dict["advanced"]["urbtix_account"].strip())
    txt_urbtix_account = Entry(frame_group_header, width=15, textvariable=txt_urbtix_account_value)
    txt_urbtix_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_urbtix_password
    txt_urbtix_password_value = StringVar(frame_group_header,
                                          value=util.decryptMe(config_dict["advanced"]["urbtix_password"].strip()))
    txt_urbtix_password = Entry(frame_group_header, width=15, textvariable=txt_urbtix_password_value, show="*")
    txt_urbtix_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_hkticketing_account
    lbl_hkticketing_account = Label(frame_group_header, text=translate[language_code]['hkticketing_account'])
    lbl_hkticketing_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_hkticketing_account
    txt_hkticketing_account_value = StringVar(frame_group_header,
                                              value=config_dict["advanced"]["hkticketing_account"].strip())
    txt_hkticketing_account = Entry(frame_group_header, width=15, textvariable=txt_hkticketing_account_value)
    txt_hkticketing_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_hkticketing_password
    txt_hkticketing_password_value = StringVar(frame_group_header, value=util.decryptMe(
        config_dict["advanced"]["hkticketing_password"].strip()))
    txt_hkticketing_password = Entry(frame_group_header, width=15, textvariable=txt_hkticketing_password_value,
                                     show="*")
    txt_hkticketing_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_kham_account
    lbl_kham_account = Label(frame_group_header, text=translate[language_code]['kham_account'])
    lbl_kham_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_kham_account
    txt_kham_account_value = StringVar(frame_group_header, value=config_dict["advanced"]["kham_account"].strip())
    txt_kham_account = Entry(frame_group_header, width=15, textvariable=txt_kham_account_value)
    txt_kham_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_kham_password
    txt_kham_password_value = StringVar(frame_group_header,
                                        value=util.decryptMe(config_dict["advanced"]["kham_password"].strip()))
    txt_kham_password = Entry(frame_group_header, width=15, textvariable=txt_kham_password_value, show="*")
    txt_kham_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_ticket_account
    lbl_ticket_account = Label(frame_group_header, text=translate[language_code]['ticket_account'])
    lbl_ticket_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_ticket_account
    txt_ticket_account_value = StringVar(frame_group_header, value=config_dict["advanced"]["ticket_account"].strip())
    txt_ticket_account = Entry(frame_group_header, width=15, textvariable=txt_ticket_account_value)
    txt_ticket_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_ticket_password
    txt_ticket_password_value = StringVar(frame_group_header,
                                          value=util.decryptMe(config_dict["advanced"]["ticket_password"].strip()))
    txt_ticket_password = Entry(frame_group_header, width=15, textvariable=txt_ticket_password_value, show="*")
    txt_ticket_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_udn_account
    lbl_udn_account = Label(frame_group_header, text=translate[language_code]['udn_account'])
    lbl_udn_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_udn_account
    txt_udn_account_value = StringVar(frame_group_header, value=config_dict["advanced"]["udn_account"].strip())
    txt_udn_account = Entry(frame_group_header, width=15, textvariable=txt_udn_account_value)
    txt_udn_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_udn_password
    txt_udn_password_value = StringVar(frame_group_header,
                                       value=util.decryptMe(config_dict["advanced"]["udn_password"].strip()))
    txt_udn_password = Entry(frame_group_header, width=15, textvariable=txt_udn_password_value, show="*")
    txt_udn_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_ticketplus_account
    lbl_ticketplus_account = Label(frame_group_header, text=translate[language_code]['ticketplus_account'])
    lbl_ticketplus_account.grid(column=0, row=group_row_count, sticky=E)

    global txt_ticketplus_account
    txt_ticketplus_account_value = StringVar(frame_group_header,
                                             value=config_dict["advanced"]["ticketplus_account"].strip())
    txt_ticketplus_account = Entry(frame_group_header, width=15, textvariable=txt_ticketplus_account_value)
    txt_ticketplus_account.grid(column=1, row=group_row_count, sticky=W)

    global txt_ticketplus_password
    txt_ticketplus_password_value = StringVar(frame_group_header, value=util.decryptMe(
        config_dict["advanced"]["ticketplus_password"].strip()))
    txt_ticketplus_password = Entry(frame_group_header, width=15, textvariable=txt_ticketplus_password_value, show="*")
    txt_ticketplus_password.grid(column=2, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_save_password_alert
    lbl_save_password_alert = Label(frame_group_header, fg="red", text=translate[language_code]['save_password_alert'])
    lbl_save_password_alert.grid(column=0, row=group_row_count, columnspan=2, sticky=E)

    frame_group_header.grid(column=0, row=row_count, padx=UI_PADDING_X)


def change_maxbot_status_by_keyword():
    config_filepath, config_dict = load_json()

    system_clock_data = datetime.now()
    current_time = system_clock_data.strftime('%H:%M:%S')
    # print('Current Time is:', current_time)
    if len(config_dict["advanced"]["idle_keyword"]) > 0:
        is_matched = util.is_text_match_keyword(config_dict["advanced"]["idle_keyword"], current_time)
        if is_matched:
            # print("match to idle:", current_time)
            do_maxbot_idle()
    if len(config_dict["advanced"]["resume_keyword"]) > 0:
        is_matched = util.is_text_match_keyword(config_dict["advanced"]["resume_keyword"], current_time)
        if is_matched:
            # print("match to resume:", current_time)
            do_maxbot_resume()

    current_time = system_clock_data.strftime('%S')
    if len(config_dict["advanced"]["idle_keyword_second"]) > 0:
        is_matched = util.is_text_match_keyword(config_dict["advanced"]["idle_keyword_second"], current_time)
        if is_matched:
            # print("match to idle:", current_time)
            do_maxbot_idle()
    if len(config_dict["advanced"]["resume_keyword_second"]) > 0:
        is_matched = util.is_text_match_keyword(config_dict["advanced"]["resume_keyword_second"], current_time)
        if is_matched:
            # print("match to resume:", current_time)
            do_maxbot_resume()

    check_maxbot_config_unsaved(config_dict)


def check_maxbot_config_unsaved(config_dict):
    # alert not saved config.
    selected_tab_index = -1

    global tabControl
    if 'tabControl' in globals():
        selected_tab_index = tabControl.index(tabControl.select())

    if selected_tab_index == 0:
        global combo_homepage
        global combo_ticket_number

        global txt_date_keyword
        global txt_area_keyword
        global txt_keyword_exclude

        global txt_date_keyword_highlightthickness
        if not 'txt_date_keyword_highlightthickness' in globals():
            txt_date_keyword_highlightthickness = 0

        global txt_area_keyword_highlightthickness
        if not 'txt_area_keyword_highlightthickness' in globals():
            txt_area_keyword_highlightthickness = 0

        global txt_keyword_exclude_highlightthickness
        if not 'txt_keyword_exclude_highlightthickness' in globals():
            txt_keyword_exclude_highlightthickness = 0

        try:
            date_keyword = ""
            if 'txt_date_keyword' in globals():
                date_keyword = txt_date_keyword.get("1.0", END).strip()
                date_keyword = util.format_config_keyword_for_json(date_keyword)

            area_keyword = ""
            if 'txt_area_keyword' in globals():
                area_keyword = txt_area_keyword.get("1.0", END).strip()
                area_keyword = util.format_config_keyword_for_json(area_keyword)

            keyword_exclude = ""
            if 'txt_keyword_exclude' in globals():
                keyword_exclude = txt_keyword_exclude.get("1.0", END).strip()
                keyword_exclude = util.format_config_keyword_for_json(keyword_exclude)

            highlightthickness = 0
            if 'combo_homepage' in globals():
                if len(combo_homepage.get().strip()) > 0:
                    if config_dict["homepage"] != combo_homepage.get().strip():
                        highlightthickness = 2

            highlightthickness = 0
            if 'combo_ticket_number' in globals():
                if len(combo_ticket_number.get().strip()) > 0:
                    if config_dict["ticket_number"] != int(combo_ticket_number.get().strip()):
                        highlightthickness = 2
            # fail, tkinter combobox border style is not working anymore
            # combo_ticket_number.config(highlightthickness=highlightthickness, highlightbackground="red")

            highlightthickness = 0
            if config_dict["date_auto_select"]["date_keyword"] != date_keyword:
                highlightthickness = 2

            if txt_date_keyword_highlightthickness != highlightthickness:
                txt_date_keyword_highlightthickness = highlightthickness
                txt_date_keyword.config(highlightthickness=highlightthickness, highlightbackground="red")

            highlightthickness = 0
            if config_dict["area_auto_select"]["area_keyword"] != area_keyword:
                highlightthickness = 2

            if txt_area_keyword_highlightthickness != highlightthickness:
                txt_area_keyword_highlightthickness = highlightthickness
                txt_area_keyword.config(highlightthickness=highlightthickness, highlightbackground="red")

            highlightthickness = 0
            if config_dict["keyword_exclude"] != keyword_exclude:
                highlightthickness = 2

            if txt_keyword_exclude_highlightthickness != highlightthickness:
                txt_keyword_exclude_highlightthickness = highlightthickness
                txt_keyword_exclude.config(highlightthickness=highlightthickness, highlightbackground="red")
        except Exception as exc:
            # print(exc)
            pass

    if selected_tab_index == 5:
        global txt_idle_keyword
        global txt_resume_keyword
        global txt_idle_keyword_second
        global txt_resume_keyword_second

        try:
            idle_keyword = ""
            if 'txt_idle_keyword' in globals():
                idle_keyword = txt_idle_keyword.get("1.0", END).strip()
                idle_keyword = util.format_config_keyword_for_json(idle_keyword)

            resume_keyword = ""
            if 'txt_resume_keyword' in globals():
                resume_keyword = txt_resume_keyword.get("1.0", END).strip()
                resume_keyword = util.format_config_keyword_for_json(resume_keyword)

            idle_keyword_second = ""
            if 'txt_idle_keyword_second' in globals():
                idle_keyword_second = txt_idle_keyword_second.get("1.0", END).strip()
                idle_keyword_second = util.format_config_keyword_for_json(idle_keyword_second)

            resume_keyword_second = ""
            if 'txt_resume_keyword_second' in globals():
                resume_keyword_second = txt_resume_keyword_second.get("1.0", END).strip()
                resume_keyword_second = util.format_config_keyword_for_json(resume_keyword_second)

            highlightthickness = 0
            if config_dict["advanced"]["idle_keyword"] != idle_keyword:
                highlightthickness = 2
            txt_idle_keyword.config(highlightthickness=highlightthickness, highlightbackground="red")

            highlightthickness = 0
            if config_dict["advanced"]["resume_keyword"] != resume_keyword:
                highlightthickness = 2
            txt_resume_keyword.config(highlightthickness=highlightthickness, highlightbackground="red")

            highlightthickness = 0
            if config_dict["advanced"]["idle_keyword_second"] != idle_keyword_second:
                highlightthickness = 2
            txt_idle_keyword_second.config(highlightthickness=highlightthickness, highlightbackground="red")

            highlightthickness = 0
            if config_dict["advanced"]["resume_keyword_second"] != resume_keyword_second:
                highlightthickness = 2
            txt_resume_keyword_second.config(highlightthickness=highlightthickness, highlightbackground="red")
        except Exception as exc:
            # print(exc)
            pass


def settings_gui_timer():
    _finished_first_loop = False
    while True:
        # btn_preview_text_clicked()
        preview_question_text_file()
        update_maxbot_runtime_status()
        change_maxbot_status_by_keyword()
        time.sleep(0.4)
        if GLOBAL_SERVER_SHUTDOWN:
            break

        if not _finished_first_loop:
            _finished_first_loop = True
            msg = f"[*INFO*] - settings_gui_timer() running successfully"
            print(msg)


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


def update_maxbot_runtime_status():
    is_paused = False
    if os.path.exists(CONST_MAXBOT_INT28_FILE):
        is_paused = True

    sync_status_to_extension(not is_paused)

    global combo_language
    global lbl_maxbot_status_data
    try:
        language_code = ""
        if 'combo_language' in globals():
            new_language = combo_language.get().strip()
            language_code = get_language_code_by_name(new_language)

        if len(language_code) > 0:
            maxbot_status = translate[language_code]['status_enabled']
            if is_paused:
                maxbot_status = translate[language_code]['status_paused']

            if 'lbl_maxbot_status_data' in globals():
                lbl_maxbot_status_data.config(text=maxbot_status)

        global btn_idle
        global btn_resume

        if not is_paused:
            btn_idle.grid(column=1, row=0)
            btn_resume.grid_forget()
        else:
            btn_resume.grid(column=2, row=0)
            btn_idle.grid_forget()

        global lbl_maxbot_last_url_data
        last_url = read_last_url_from_file()
        if len(last_url) > 60:
            last_url = last_url[:60] + "..."
        if 'lbl_maxbot_last_url_data' in globals():
            lbl_maxbot_last_url_data.config(text=last_url)

        system_clock_data = datetime.now()
        current_time = system_clock_data.strftime('%H:%M:%S')
        # print('Current Time is:', current_time)

        global lbl_system_clock_data
        if 'lbl_system_clock_data' in globals():
            lbl_system_clock_data.config(text=current_time)

    except Exception as exc:
        # print(exc)
        pass


def RuntimeTab(root, config_dict, language_code, UI_PADDING_X):
    row_count = 0

    frame_group_header = Frame(root)
    group_row_count = 0

    maxbot_status = ""
    global lbl_maxbot_status
    lbl_maxbot_status = Label(frame_group_header, text=translate[language_code]['running_status'])
    lbl_maxbot_status.grid(column=0, row=group_row_count, sticky=E)

    frame_maxbot_interrupt = Frame(frame_group_header)

    global lbl_maxbot_status_data
    lbl_maxbot_status_data = Label(frame_maxbot_interrupt, text=maxbot_status)
    lbl_maxbot_status_data.grid(column=0, row=group_row_count, sticky=W)

    global btn_idle
    global btn_resume

    btn_idle = ttk.Button(frame_maxbot_interrupt, text=translate[language_code]['idle'],
                          command=lambda: btn_idle_clicked(language_code))
    btn_idle.grid(column=1, row=0)

    btn_resume = ttk.Button(frame_maxbot_interrupt, text=translate[language_code]['resume'],
                            command=lambda: btn_resume_clicked(language_code))
    btn_resume.grid(column=2, row=0)

    frame_maxbot_interrupt.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_maxbot_last_url
    lbl_maxbot_last_url = Label(frame_group_header, text=translate[language_code]['running_url'])
    lbl_maxbot_last_url.grid(column=0, row=group_row_count, sticky=E)

    last_url = ""
    global lbl_maxbot_last_url_data
    lbl_maxbot_last_url_data = Label(frame_group_header, text=last_url)
    lbl_maxbot_last_url_data.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_system_clock
    lbl_system_clock = Label(frame_group_header, text=translate[language_code]['system_clock'])
    lbl_system_clock.grid(column=0, row=group_row_count, sticky=E)

    system_clock = ""
    global lbl_system_clock_data
    lbl_system_clock_data = Label(frame_group_header, text=system_clock)
    lbl_system_clock_data.grid(column=1, row=group_row_count, sticky=W)

    group_row_count += 1

    global lbl_idle_keyword
    lbl_idle_keyword = Label(frame_group_header, text=translate[language_code]['idle_keyword'])
    lbl_idle_keyword.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_idle_keyword
    txt_idle_keyword = Text(frame_group_header, width=30, height=4)
    txt_idle_keyword.grid(column=1, row=group_row_count, sticky=W)
    txt_idle_keyword.insert("1.0", config_dict["advanced"]["idle_keyword"].strip())

    group_row_count += 1

    global lbl_resume_keyword
    lbl_resume_keyword = Label(frame_group_header, text=translate[language_code]['resume_keyword'])
    lbl_resume_keyword.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_resume_keyword
    txt_resume_keyword = Text(frame_group_header, width=30, height=4)
    txt_resume_keyword.grid(column=1, row=group_row_count, sticky=W)
    txt_resume_keyword.insert("1.0", config_dict["advanced"]["resume_keyword"].strip())

    group_row_count += 1

    global lbl_idle_keyword_second
    lbl_idle_keyword_second = Label(frame_group_header, text=translate[language_code]['idle_keyword_second'])
    lbl_idle_keyword_second.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_idle_keyword_second
    txt_idle_keyword_second = Text(frame_group_header, width=30, height=4)
    txt_idle_keyword_second.grid(column=1, row=group_row_count, sticky=W)
    txt_idle_keyword_second.insert("1.0", config_dict["advanced"]["idle_keyword_second"].strip())

    group_row_count += 1

    global lbl_resume_keyword_second
    lbl_resume_keyword_second = Label(frame_group_header, text=translate[language_code]['resume_keyword_second'])
    lbl_resume_keyword_second.grid(column=0, row=group_row_count, sticky=E + N)

    global txt_resume_keyword_second
    txt_resume_keyword_second = Text(frame_group_header, width=30, height=4)
    txt_resume_keyword_second.grid(column=1, row=group_row_count, sticky=W)
    txt_resume_keyword_second.insert("1.0", config_dict["advanced"]["resume_keyword_second"].strip())

    frame_group_header.grid(column=0, row=row_count, padx=UI_PADDING_X)
    update_maxbot_runtime_status()


def AboutTab(root, language_code):
    row_count = 0

    frame_group_header = Frame(root)
    group_row_count = 0

    logo_filename = "maxbot_logo2_single.ppm"
    logo_img = PhotoImage(file=logo_filename)

    lbl_logo = Label(frame_group_header, image=logo_img)
    lbl_logo.image = logo_img
    lbl_logo.grid(column=0, row=group_row_count, columnspan=2)

    group_row_count += 1

    global lbl_slogan
    global lbl_help
    global lbl_donate
    global lbl_release

    lbl_slogan = Label(frame_group_header, text=translate[language_code]['maxbot_slogan'], wraplength=400,
                       justify="center")
    lbl_slogan.grid(column=0, row=group_row_count, columnspan=2)

    group_row_count += 1

    lbl_help = Label(frame_group_header, text=translate[language_code]['help'])
    lbl_help.grid(column=0, row=group_row_count, sticky=E)

    lbl_help_url = Label(frame_group_header, text=URL_HELP, fg="blue", bg="gray", cursor="hand2")
    lbl_help_url.grid(column=1, row=group_row_count, sticky=W)
    lbl_help_url.bind("<Button-1>", lambda e: open_url(URL_HELP))

    group_row_count += 1

    lbl_donate = Label(frame_group_header, text=translate[language_code]['donate'])
    lbl_donate.grid(column=0, row=group_row_count, sticky=E)

    lbl_donate_url = Label(frame_group_header, text=URL_DONATE, fg="blue", bg="gray", cursor="hand2")
    lbl_donate_url.grid(column=1, row=group_row_count, sticky=W)
    lbl_donate_url.bind("<Button-1>", lambda e: open_url(URL_DONATE))

    group_row_count += 1

    lbl_release = Label(frame_group_header, text=translate[language_code]['release'])
    lbl_release.grid(column=0, row=group_row_count, sticky=E)

    lbl_release_url = Label(frame_group_header, text=URL_RELEASE, fg="blue", bg="gray", cursor="hand2")
    lbl_release_url.grid(column=1, row=group_row_count, sticky=W)
    lbl_release_url.bind("<Button-1>", lambda e: open_url(URL_RELEASE))

    group_row_count += 1

    lbl_fb_fans = Label(frame_group_header, text=u'Facebook')
    lbl_fb_fans.grid(column=0, row=group_row_count, sticky=E)

    lbl_fb_fans_url = Label(frame_group_header, text=URL_FB, fg="blue", bg="gray", cursor="hand2")
    lbl_fb_fans_url.grid(column=1, row=group_row_count, sticky=W)
    lbl_fb_fans_url.bind("<Button-1>", lambda e: open_url(URL_FB))

    group_row_count += 1

    lbl_chrome_driver = Label(frame_group_header, text=u'Chrome Driver')
    lbl_chrome_driver.grid(column=0, row=group_row_count, sticky=E)

    lbl_chrome_driver_url = Label(frame_group_header, text=URL_CHROME_DRIVER, fg="blue", bg="gray", cursor="hand2")
    lbl_chrome_driver_url.grid(column=1, row=group_row_count, sticky=W)
    lbl_chrome_driver_url.bind("<Button-1>", lambda e: open_url(URL_CHROME_DRIVER))

    group_row_count += 1

    lbl_firefox_driver = Label(frame_group_header, text=u'Firefox Driver')
    lbl_firefox_driver.grid(column=0, row=group_row_count, sticky=E)

    lbl_firefox_driver_url = Label(frame_group_header, text=URL_FIREFOX_DRIVER, fg="blue", bg="gray", cursor="hand2")
    lbl_firefox_driver_url.grid(column=1, row=group_row_count, sticky=W)
    lbl_firefox_driver_url.bind("<Button-1>", lambda e: open_url(URL_FIREFOX_DRIVER))

    group_row_count += 1

    lbl_edge_driver = Label(frame_group_header, text=u'Edge Driver')
    lbl_edge_driver.grid(column=0, row=group_row_count, sticky=E)

    lbl_edge_driver_url = Label(frame_group_header, text=URL_EDGE_DRIVER, fg="blue", bg="gray", cursor="hand2")
    lbl_edge_driver_url.grid(column=1, row=group_row_count, sticky=W)
    lbl_edge_driver_url.bind("<Button-1>", lambda e: open_url(URL_EDGE_DRIVER))

    frame_group_header.grid(column=0, row=row_count)


def get_action_bar(root, language_code):
    """
    primary buttons defined functino
    """
    frame_action = Frame(root)

    global btn_run
    global btn_save
    global btn_exit
    global btn_restore_defaults
    global btn_launcher

    btn_run = ttk.Button(frame_action, text=translate[language_code]['run'], command=btn_run_clicked)
    btn_run.grid(column=0, row=0)

    btn_save = ttk.Button(frame_action, text=translate[language_code]['save'], command=btn_save_clicked)
    btn_save.grid(column=1, row=0)

    btn_exit = ttk.Button(frame_action, text=translate[language_code]['exit'], command=btn_exit_clicked)
    # btn_exit.grid(column=2, row=0)

    btn_launcher = ttk.Button(frame_action, text=translate[language_code]['config_launcher'],
                              command=btn_launcher_clicked)
    btn_launcher.grid(column=2, row=0)

    btn_restore_defaults = ttk.Button(frame_action, text=translate[language_code]['restore_defaults'],
                                      command=btn_restore_defaults_clicked)
    btn_restore_defaults.grid(column=3, row=0)

    return frame_action


def clearFrame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
        widget.destroy()


def load_GUI(root, config_dict):
    clearFrame(root)

    language_code = "en_us"
    if not config_dict is None:
        if u'language' in config_dict:
            language_code = get_language_code_by_name(config_dict["language"])

    row_count = 0

    global tabControl
    tabControl = ttk.Notebook(root)
    tab1 = Frame(tabControl)
    tabControl.add(tab1, text=translate[language_code]['preference'])

    tab2 = Frame(tabControl)
    tabControl.add(tab2, text=translate[language_code]['advanced'])

    tab3 = Frame(tabControl)
    tabControl.add(tab3, text=translate[language_code]['verification_word'])

    global tab4
    tab4 = Frame(tabControl)
    tabControl.add(tab4, text=translate[language_code]['maxbot_server'])

    tab5 = Frame(tabControl)
    tabControl.add(tab5, text=translate[language_code]['autofill'])

    tab6 = Frame(tabControl)
    tabControl.add(tab6, text=translate[language_code]['runtime'])

    tab7 = Frame(tabControl)
    tabControl.add(tab7, text=translate[language_code]['about'])

    tabControl.grid(column=0, row=row_count)
    tabControl.select(tab1)

    row_count += 1

    frame_action = get_action_bar(root, language_code)
    frame_action.grid(column=0, row=row_count)

    global UI_PADDING_X
    PreferenctTab(tab1, config_dict, language_code, UI_PADDING_X)
    AdvancedTab(tab2, config_dict, language_code, UI_PADDING_X)
    VerificationTab(tab3, config_dict, language_code, UI_PADDING_X)
    ServerTab(tab4, config_dict, language_code, UI_PADDING_X)
    AutofillTab(tab5, config_dict, language_code, UI_PADDING_X)
    RuntimeTab(tab6, config_dict, language_code, UI_PADDING_X)
    AboutTab(tab7, language_code)


def main_gui():
    global translate
    translate = load_translate()

    global config_filepath
    global config_dict
    config_filepath, config_dict = load_json()

    global root
    root = Tk()
    # root = customtkinter.CTk()
    root.title(CONST_APP_VERSION)

    global UI_PADDING_X
    UI_PADDING_X = 15

    load_GUI(root, config_dict)

    GUI_SIZE_WIDTH = 610
    GUI_SIZE_HEIGHT = 645

    GUI_SIZE_MACOS = str(GUI_SIZE_WIDTH) + 'x' + str(GUI_SIZE_HEIGHT)
    GUI_SIZE_WINDOWS = str(GUI_SIZE_WIDTH - 70) + 'x' + str(GUI_SIZE_HEIGHT - 80)
    GUI_SIZE_LINUX = str(GUI_SIZE_WIDTH - 50) + 'x' + str(GUI_SIZE_HEIGHT - 140)

    GUI_SIZE = GUI_SIZE_MACOS
    if platform.system() == 'Windows':
        GUI_SIZE = GUI_SIZE_WINDOWS
    if platform.system() == 'Linux':
        GUI_SIZE = GUI_SIZE_LINUX

    root.geometry(GUI_SIZE)

    # icon format.
    default_icon_path = PROJECT_DIR / 'asset' / 'max-icon-base64.txt'
    with open(default_icon_path, 'r') as f:
        icon_img = f.read()

    if platform.system() == 'Linux':
        linux_icon_path = PROJECT_DIR / 'asset' / 'max-icon-linux-base64.txt'
        with open(linux_icon_path, 'r') as f:
            icon_img = f.read()

    icon_filepath = 'tmp.ico'
    temp_icon = open(icon_filepath, 'wb+')
    temp_icon.write(base64.b64decode(icon_img))
    temp_icon.close()
    if platform.system() == 'Windows':
        root.iconbitmap(icon_filepath)
    if platform.system() == 'Darwin':
        # from PIL import Image, ImageTk
        # logo = ImageTk.PhotoImage(Image.open(icon_filepath).convert('RGB'))
        # root.call('wm', 'iconphoto', root._w, logo)
        pass
    if platform.system() == 'Linux':
        logo = PhotoImage(file=icon_filepath)
        root.call('wm', 'iconphoto', root._w, logo)
    os.remove(icon_filepath)

    root.mainloop()
    GLOBAL_SERVER_SHUTDOWN = True
    clean_extension_status()


def clean_tmp_file():
    remove_file_list = [
        CONST_MAXBOT_LAST_URL_FILE,
        CONST_MAXBOT_INT28_FILE,
        CONST_MAXBOT_ANSWER_ONLINE_FILE,
        CONST_MAXBOT_QUESTION_FILE
    ]
    for filepath in remove_file_list:
        util.force_remove_file(filepath)


def btn_copy_ip_clicked():
    local_ip = util.get_ip_address()
    ip_address = "http://%s:%d/" % (local_ip, CONST_SERVER_PORT)
    pyperclip.copy(ip_address)


def btn_copy_question_clicked():
    global txt_question
    question_text = txt_question.get("1.0", END).strip()
    if len(question_text) > 0:
        pyperclip.copy(question_text)


def btn_query_question_clicked():
    global txt_question
    question_text = txt_question.get("1.0", END).strip()
    if len(question_text) > 0:
        webbrowser.open("https://www.google.com/search?q=" + question_text)


class MainHandler(tornado.web.RequestHandler):
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


class QuestionHandler(tornado.web.RequestHandler):
    def get(self):
        global txt_question
        txt_question.insert("1.0", "")


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"version": self.application.version})


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
                print("ocr_answer:", ocr_answer)
            except Exception as exc:
                pass

        self.write({"answer": ocr_answer})


async def main_server():
    ocr = None
    try:
        ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
    except Exception as exc:
        print(exc)
        pass

    app = Application([
        ("/", MainHandler),
        ("/version", VersionHandler),
        ("/ocr", OcrHandler),
        ("/query", MainHandler),
        ("/question", QuestionHandler),
    ])
    app.ocr = ocr
    app.version = CONST_APP_VERSION

    app.listen(CONST_SERVER_PORT)

    msg = f"[*INFO*] - server running on port: {CONST_SERVER_PORT}"
    print(msg)

    await asyncio.Event().wait()


def launch_web_server():
    host = 'localhost'
    port = CONST_SERVER_PORT
    is_port_bound = network_tool.port_is_connectable(
        host=host,
        port=port
    )

    if not is_port_bound:
        asyncio.run(main_server())

    else:
        msg = f"[*WARN*] - port: {CONST_SERVER_PORT} on host: {host} is already in used"
        raise RuntimeError(msg)


def preview_question_text_file():
    if os.path.exists(CONST_MAXBOT_QUESTION_FILE):
        infile = None
        if platform.system() == 'Windows':
            infile = open(CONST_MAXBOT_QUESTION_FILE, 'r', encoding='UTF-8')
        else:
            infile = open(CONST_MAXBOT_QUESTION_FILE, 'r')

        if not infile is None:
            question_text = infile.readline()

            global txt_question
            if 'txt_question' in globals():
                try:
                    displayed_question_text = txt_question.get("1.0", END).strip()
                    if displayed_question_text != question_text:
                        # start to refresh
                        txt_question.delete("1.0", "end")
                        if len(question_text) > 0:
                            txt_question.insert("1.0", question_text)
                except Exception as exc:
                    pass


if __name__ == "__main__":
    daemon = False
    threading.Thread(target=settings_gui_timer, daemon=daemon).start()
    threading.Thread(target=launch_web_server, daemon=daemon).start()

    clean_tmp_file()
    main_gui()
