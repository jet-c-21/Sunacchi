from typing import List, Dict, Any, Tuple, Optional
import base64
import json
import os
import pathlib
import platform
import random
import re
import socket
import subprocess
import sys
import threading

import requests

CONST_FROM_TOP_TO_BOTTOM = "from top to bottom"
CONST_FROM_BOTTOM_TO_TOP = "from bottom to top"
CONST_CENTER = "center"
CONST_RANDOM = "random"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def get_ip_address():
    gethostname = None
    try:
        gethostname = socket.gethostname()
    except Exception as exc:
        print("gethostname", exc)
        gethostname = None

    default_ip = "127.0.0.1"
    ip = default_ip

    check_public_ip = True
    if "macos" in platform.platform().lower():
        if "arm64" in platform.platform().lower():
            check_public_ip = False

    if check_public_ip and not gethostname is None:
        try:
            ip = [l for l in ([ip for ip in socket.gethostbyname_ex(gethostname)[2]
                               if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
                                                                     s.getsockname()[0], s.close()) for s in
                                                                    [socket.socket(socket.AF_INET,
                                                                                   socket.SOCK_DGRAM)]][0][1]]) if l][
                0][0]
        except Exception as exc:
            print("gethostbyname_ex", exc)
            ip = gethostname

    # print("get_ip_address:", ip)
    return ip


def remove_html_tags(text):
    ret = ""
    if not text is None:
        clean = re.compile('<.*?>')
        ret = re.sub(clean, '', text)
        ret = ret.strip()
    return ret


# common functions.
def find_between(s, first, last):
    ret = ""
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        ret = s[start:end]
    except ValueError:
        pass
    return ret


def sx(s1):
    key = 18
    return ''.join(chr(ord(a) ^ key) for a in s1)


def decryptMe(b):
    s = ""
    if (len(b) > 0):
        s = sx(base64.b64decode(b).decode("UTF-8"))
    return s


def encryptMe(s):
    data = ""
    if (len(s) > 0):
        data = base64.b64encode(sx(s).encode('UTF-8')).decode("UTF-8")
    return data


def format_config_keyword_for_json(user_input):
    if len(user_input) > 0:
        if not ('\"' in user_input):
            user_input = '"' + user_input + '"'

        if user_input[:1] == "{" and user_input[-1:] == "}":
            tmp_json = {}
            try:
                tmp_json = json.loads(user_input)
                key = list(tmp_json.keys())[0]
                first_item = tmp_json[key]
                user_input = json.dumps(first_item)
            except Exception as exc:
                pass

        if user_input[:1] == "[" and user_input[-1:] == "]":
            user_input = user_input[1:]
            user_input = user_input[:-1]
    return user_input


def is_text_match_keyword(keyword_string, text):
    is_match_keyword = True
    if len(keyword_string) > 0 and len(text) > 0:

        # directly input text into arrray field.
        if len(keyword_string) > 0:
            if not '"' in keyword_string:
                keyword_string = '"' + keyword_string + '"'

        is_match_keyword = False
        keyword_array = []
        try:
            keyword_array = json.loads("[" + keyword_string + "]")
        except Exception as exc:
            keyword_array = []
        for item_list in keyword_array:
            if len(item_list) > 0:
                if ' ' in item_list:
                    keyword_item_array = item_list.split(' ')
                    is_match_all = True
                    for each_item in keyword_item_array:
                        if not each_item in text:
                            is_match_all = False
                    if is_match_all:
                        is_match_keyword = True
                else:
                    if item_list in text:
                        is_match_keyword = True
            else:
                is_match_keyword = True
            if is_match_keyword:
                break
    return is_match_keyword


def save_json(config_dict, target_path):
    json_str = json.dumps(config_dict, indent=4)
    try:
        with open(target_path, 'w') as outfile:
            outfile.write(json_str)
    except Exception as e:
        pass


def write_string_to_file(filename, data):
    outfile = None
    if platform.system() == 'Windows':
        outfile = open(filename, 'w', encoding='UTF-8')
    else:
        outfile = open(filename, 'w')

    if not outfile is None:
        outfile.write("%s" % data)


def save_url_to_file(remote_url, CONST_MAXBOT_ANSWER_ONLINE_FILE, force_write=False, timeout=0.5):
    html_text = ""
    if len(remote_url) > 0:
        html_result = None
        try:
            html_result = requests.get(remote_url, timeout=timeout, allow_redirects=False)
        except Exception as exc:
            html_result = None
            # print(exc)
        if not html_result is None:
            status_code = html_result.status_code
            # print("status_code:", status_code)
            if status_code == 200:
                html_text = html_result.text
                # print("html_text:", html_text)

    is_write_to_file = False
    if force_write:
        is_write_to_file = True
    if len(html_text) > 0:
        is_write_to_file = True

    if is_write_to_file:
        html_text = format_config_keyword_for_json(html_text)
        working_dir = os.path.dirname(os.path.realpath(__file__))
        target_path = os.path.join(working_dir, CONST_MAXBOT_ANSWER_ONLINE_FILE)
        write_string_to_file(target_path, html_text)
    return is_write_to_file


def play_mp3_async(sound_filename):
    threading.Thread(target=play_mp3, args=(sound_filename,)).start()


def play_mp3(sound_filename):
    from playsound import playsound
    try:
        playsound(sound_filename)
    except Exception as exc:
        msg = str(exc)
        # print("play sound exeption:", msg)
        if platform.system() == 'Windows':
            import winsound
            try:
                winsound.PlaySound(sound_filename, winsound.SND_FILENAME)
            except Exception as exc2:
                pass


def force_remove_file(filepath):
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as exc:
            pass


def clean_uc_exe_cache():
    exe_name = "chromedriver%s"

    platform = sys.platform
    if platform.endswith("win32"):
        exe_name %= ".exe"
    if platform.endswith(("linux", "linux2")):
        exe_name %= ""
    if platform.endswith("darwin"):
        exe_name %= ""

    d = ""
    if platform.endswith("win32"):
        d = "~/appdata/roaming/undetected_chromedriver"
    elif "LAMBDA_TASK_ROOT" in os.environ:
        d = "/tmp/undetected_chromedriver"
    elif platform.startswith(("linux", "linux2")):
        d = "~/.local/share/undetected_chromedriver"
    elif platform.endswith("darwin"):
        d = "~/Library/Application Support/undetected_chromedriver"
    else:
        d = "~/.undetected_chromedriver"
    data_path = os.path.abspath(os.path.expanduser(d))

    is_cache_exist = False
    p = pathlib.Path(data_path)
    files = list(p.rglob("*chromedriver*?"))
    for file in files:
        if os.path.exists(str(file)):
            is_cache_exist = True
            try:
                os.unlink(str(file))
            except Exception as exc2:
                print(exc2)
                pass

    return is_cache_exist


def t_or_f(arg):
    ret = False
    ua = str(arg).upper()
    if 'TRUE'.startswith(ua):
        ret = True
    elif 'YES'.startswith(ua):
        ret = True
    return ret


def format_keyword_string(keyword):
    if not keyword is None:
        if len(keyword) > 0:
            keyword = keyword.replace('／', '/')
            keyword = keyword.replace('　', '')
            keyword = keyword.replace(',', '')
            keyword = keyword.replace('，', '')
            keyword = keyword.replace('$', '')
            keyword = keyword.replace(' ', '').lower()
    return keyword


def format_quota_string(formated_html_text):
    formated_html_text = formated_html_text.replace('「', '【')
    formated_html_text = formated_html_text.replace('『', '【')
    formated_html_text = formated_html_text.replace('〔', '【')
    formated_html_text = formated_html_text.replace('﹝', '【')
    formated_html_text = formated_html_text.replace('〈', '【')
    formated_html_text = formated_html_text.replace('《', '【')
    formated_html_text = formated_html_text.replace('［', '【')
    formated_html_text = formated_html_text.replace('〖', '【')
    formated_html_text = formated_html_text.replace('[', '【')
    formated_html_text = formated_html_text.replace('（', '【')
    formated_html_text = formated_html_text.replace('(', '【')

    formated_html_text = formated_html_text.replace('」', '】')
    formated_html_text = formated_html_text.replace('』', '】')
    formated_html_text = formated_html_text.replace('〕', '】')
    formated_html_text = formated_html_text.replace('﹞', '】')
    formated_html_text = formated_html_text.replace('〉', '】')
    formated_html_text = formated_html_text.replace('》', '】')
    formated_html_text = formated_html_text.replace('］', '】')
    formated_html_text = formated_html_text.replace('〗', '】')
    formated_html_text = formated_html_text.replace(']', '】')
    formated_html_text = formated_html_text.replace('）', '】')
    formated_html_text = formated_html_text.replace(')', '】')
    return formated_html_text


def full2half(keyword):
    n = ""
    if not keyword is None:
        if len(keyword) > 0:
            for char in keyword:
                num = ord(char)
                if num == 0x3000:
                    num = 32
                elif 0xFF01 <= num <= 0xFF5E:
                    num -= 0xfee0
                n += chr(num)
    return n


def get_chinese_numeric():
    my_dict = {}
    my_dict['0'] = ['0', '０', 'zero', '零']
    my_dict['1'] = ['1', '１', 'one', '一', '壹', '①', '❶', '⑴']
    my_dict['2'] = ['2', '２', 'two', '二', '貳', '②', '❷', '⑵']
    my_dict['3'] = ['3', '３', 'three', '三', '叁', '③', '❸', '⑶']
    my_dict['4'] = ['4', '４', 'four', '四', '肆', '④', '❹', '⑷']
    my_dict['5'] = ['5', '５', 'five', '五', '伍', '⑤', '❺', '⑸']
    my_dict['6'] = ['6', '６', 'six', '六', '陸', '⑥', '❻', '⑹']
    my_dict['7'] = ['7', '７', 'seven', '七', '柒', '⑦', '❼', '⑺']
    my_dict['8'] = ['8', '８', 'eight', '八', '捌', '⑧', '❽', '⑻']
    my_dict['9'] = ['9', '９', 'nine', '九', '玖', '⑨', '❾', '⑼']
    return my_dict


# 同義字
def synonym_dict(char):
    ret = []
    my_dict = get_chinese_numeric()
    if char in my_dict:
        ret = my_dict[char]
    else:
        ret.append(char)
    return ret


def chinese_numeric_to_int(char):
    ret = None
    my_dict = get_chinese_numeric()
    for i in my_dict:
        for item in my_dict[i]:
            if char.lower() == item:
                ret = int(i)
                break
        if not ret is None:
            break
    return ret


def normalize_chinese_numeric(keyword):
    ret = ""
    for char in keyword:
        converted_int = chinese_numeric_to_int(char)
        if not converted_int is None:
            ret += str(converted_int)
    return ret


def find_continuous_number(text):
    chars = "0123456789"
    return find_continuous_pattern(chars, text)


def find_continuous_text(text):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return find_continuous_pattern(chars, text)


def find_continuous_pattern(allowed_char, text):
    ret = ""
    is_allowed_char_start = False
    for char in text:
        # print("char:", char)
        if char in allowed_char:
            if len(ret) == 0 and not is_allowed_char_start:
                is_allowed_char_start = True
            if is_allowed_char_start:
                ret += char
        else:
            # make not continuous
            is_allowed_char_start = False
    return ret


def is_all_alpha_or_numeric(text):
    ret = False
    alpha_count = 0
    numeric_count = 0
    for char in text:
        try:
            if char.encode('UTF-8').isalpha():
                alpha_count += 1
        except Exception as exc:
            pass

        # if char.isnumeric():
        if char.isdigit():
            numeric_count += 1

    if (alpha_count + numeric_count) == len(text):
        ret = True

    # print("text/is_all_alpha_or_numeric:",text,ret)
    return ret


def get_brave_bin_path():
    brave_path = ""
    if platform.system() == 'Windows':
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        if not os.path.exists(brave_path):
            brave_path = os.path.expanduser(
                '~') + "\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        if not os.path.exists(brave_path):
            brave_path = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        if not os.path.exists(brave_path):
            brave_path = "D:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

    if platform.system() == 'Linux':
        brave_path = "/usr/bin/brave-browser"

    if platform.system() == 'Darwin':
        brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'

    return brave_path


def convert_string_to_pattern(input_str, dynamic_length=True):
    hint_answer_length = len(input_str)
    formatted_pattern = ""

    if hint_answer_length > 0:
        answer_symbols = r"()[]<>{}-"
        upper_case_pattern = re.compile(r"[A-Z]")
        lower_case_pattern = re.compile(r"[a-z]")
        digit_pattern = re.compile(r"\d")

        for char in input_str:
            if char in answer_symbols:
                formatted_pattern += '\\' + char
            elif upper_case_pattern.match(char):
                formatted_pattern += "[A-Z]"
            elif lower_case_pattern.match(char):
                formatted_pattern += "[a-z]"
            elif digit_pattern.match(char):
                formatted_pattern += r"\d"

        # For dynamic length, reduce consecutive patterns and apply '+' for repetition
        if dynamic_length:
            for _ in range(10):  # Ensure replacement happens for long sequences
                formatted_pattern = formatted_pattern.replace("[A-Z][A-Z]", "[A-Z]")
                formatted_pattern = formatted_pattern.replace("[a-z][a-z]", "[a-z]")
                formatted_pattern = formatted_pattern.replace(r"\d\d", r"\d")

            formatted_pattern = formatted_pattern.replace("[A-Z]", "[A-Z]+")
            formatted_pattern = formatted_pattern.replace("[a-z]", "[a-z]+")
            formatted_pattern = formatted_pattern.replace(r"\d", r"\d+")

    return formatted_pattern


def guess_answer_list_from_multi_options(tmp_text):
    show_debug_message = False  # Set to True for debugging

    options_list = []
    matched_pattern = ""
    patterns = [
        (r'【.{1,4}】', '【', '】'),
        (r'\(.{1,4}\)', '(', ')'),
        (r'\[{1,4}\]', '[', ']'),
        (r'\\n.{1,4}\)', "\n", ')'),
        (r'\\n.{1,4}\]', "\n", ']'),
        (r'\\n.{1,4}】', "\n", '】'),
        (r'\\n.{1,4}:', "\n", ':'),
    ]

    # Match patterns in sequence
    for pattern, start_symbol, end_symbol in patterns:
        if not options_list and start_symbol in tmp_text and end_symbol in tmp_text:
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) > 2:
                matched_pattern = pattern
                break

    # Custom pattern if no options found
    if not options_list and " " in tmp_text and '?' in tmp_text:
        if any(symbol in tmp_text for symbol in ['.', ':', ')', ']', '>']):
            pattern = r"[ /\n\|;\.\?]{1}.{1}[\.:)\]>]{1}.{2,3}"
            options_list = re.findall(pattern, tmp_text)
            if len(options_list) > 2:
                options_list = [opt.strip(" .?|;:/")[:1] for opt in options_list]
                matched_pattern = pattern

    if show_debug_message:
        print(f"Matched pattern: {matched_pattern}")

    # Default quota trimming
    is_trim_quota = not check_answer_keep_symbol(tmp_text)

    if show_debug_message:
        print(f"Trim Quota: {is_trim_quota}")

    return_list = []
    if len(options_list) > 2:
        is_all_options_same_length = all(
            len(options_list[i]) == len(options_list[i + 1]) for i in range(len(options_list) - 1)
        )

        if show_debug_message:
            print(f"All options same length: {is_all_options_same_length}")

        if is_all_options_same_length:
            return_list = [opt[1:-1] if is_trim_quota else opt for opt in options_list if len(opt) > 2]
        else:
            length_counts = {len(opt): options_list.count(opt) for opt in options_list}
            target_length = max(length_counts, key=length_counts.get)
            return_list = [opt[1:-1] if is_trim_quota else opt for opt in options_list if len(opt) == target_length]

    # If only two options, reset the list
    if len(return_list) <= 2:
        return_list = []

    # Remove non-alphanumeric options
    return_list = [opt for opt in return_list if is_all_alpha_or_numeric(opt)] if len(return_list) > 2 else []

    return return_list


# PS: this may get a wrong answer list. XD
def guess_answer_list_from_symbols(captcha_text_div_text) -> List:
    return_list = []

    # Replace specific characters with spaces to normalize input
    tmp_text = captcha_text_div_text.replace('?', ' ').replace('？', ' ').replace('。', ' ')

    delimiter_symbols_left = ["(", "[", "{", " ", " ", " ", " "]
    delimiter_symbols_right = [")", "]", "}", ":", ".", ")", "-"]

    # Iterate over symbol pairs
    for idx in range(len(delimiter_symbols_left)):
        symbol_left = delimiter_symbols_left[idx]
        symbol_right = delimiter_symbols_right[idx]

        # Check if the current pair of symbols is in the text and if '半形' is present
        if symbol_left in tmp_text and symbol_right in tmp_text and '半形' in tmp_text:
            # hint_list = re.findall(rf'\{re.escape(symbol_left)}[\w]+\{re.escape(symbol_right)}', tmp_text) # old one
            hint_list = re.findall(rf'{re.escape(symbol_left)}[\w]+{re.escape(symbol_right)}', tmp_text)

            # If matching hints found, process and store them
            if hint_list and len(hint_list) > 1:
                return_list = []
                for option in hint_list:
                    if len(option) > 2:
                        answer = option[1:-1]  # Remove the surrounding delimiters
                        if answer:
                            return_list.append(answer)

        # Exit the loop if valid results are found
        if return_list:
            break

    return return_list


def get_official_hint_string_from_symbol(symbol, tmp_text) -> str:
    # show_debug_message = True
    show_debug_message = False  # Change to True for debugging

    official_hint_string = ""

    # Check if the symbol exists in the provided text
    if symbol in tmp_text:
        # Try to find the hint enclosed by 【】 brackets
        if not official_hint_string:
            if '【' in tmp_text and '】' in tmp_text:
                hint_list = re.findall(r'【.*?】', tmp_text)
                if show_debug_message:
                    print("【.*?】hint_list:", hint_list)
                for hint in hint_list:
                    if symbol in hint:
                        official_hint_string = hint[1:-1]  # Remove the 【 and 】 symbols
                        break

        # Try to find the hint enclosed by parentheses ()
        if not official_hint_string:
            if '(' in tmp_text and ')' in tmp_text:
                hint_list = re.findall(r'\(.*?\)', tmp_text)
                if show_debug_message:
                    print("(.*?) hint_list:", hint_list)

                for hint in hint_list:
                    if symbol in hint:
                        official_hint_string = hint[1:-1]  # Remove the ( and ) symbols
                        break

        # Try to find the hint enclosed by square brackets []
        if not official_hint_string:
            if '[' in tmp_text and ']' in tmp_text:
                hint_list = re.findall(r'\[.*?\]', tmp_text)
                if show_debug_message:
                    print("[.*?]hint_list:", hint_list)
                for hint in hint_list:
                    if symbol in hint:
                        official_hint_string = hint[1:-1]  # Remove the [ and ] symbols
                        break

        # If no specific hint was found, return the original text
        if not official_hint_string:
            official_hint_string = tmp_text

    return official_hint_string


def guess_answer_list_from_hint(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text) -> Tuple[List, str]:
    show_debug_message = False  # Change to True for debugging

    tmp_text = format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)

    my_question = ""
    my_options = ""
    official_hint_string = ""
    official_hint_string_answer = ""
    my_answer_formatted = ""
    my_answer_delimiter = ""

    # Extract question from the text
    if not my_question:
        question_index = tmp_text.find("?")
        if question_index != -1:
            my_question = tmp_text[:question_index + 1]
        else:
            question_index = tmp_text.find("。")
            if question_index != -1:
                my_question = tmp_text[:question_index + 1]
            else:
                my_question = tmp_text

    # Extract official hint string based on symbol
    if not official_hint_string and '答案' in tmp_text and CONST_INPUT_SYMBOL in tmp_text:
        official_hint_string = get_official_hint_string_from_symbol(CONST_INPUT_SYMBOL, tmp_text)
        if official_hint_string:
            right_part = official_hint_string.split(CONST_INPUT_SYMBOL)[1]
            if len(official_hint_string) == len(tmp_text):
                official_hint_string = right_part
            official_hint_string_answer = find_continuous_text(right_part)

    if not official_hint_string:
        official_hint_string = get_official_hint_string_from_symbol(CONST_EXAMPLE_SYMBOL, tmp_text)
        if official_hint_string:
            right_part = official_hint_string.split(CONST_EXAMPLE_SYMBOL)[1]
            if len(official_hint_string) == len(tmp_text):
                official_hint_string = right_part
            official_hint_string_answer = find_continuous_text(right_part)

    # Resize the hint string for options
    if official_hint_string_answer:
        official_hint_string = official_hint_string.split(official_hint_string_answer)[0]

    if show_debug_message:
        print("official_hint_string:", official_hint_string)

    # Apply additional rule to extract the hint based on "*"
    if not official_hint_string and "*" in tmp_text:
        star_index = tmp_text.find("*")
        space_index = tmp_text.find(" ", star_index + 1)
        official_hint_string = tmp_text[star_index:space_index]

    # Merge with the next block if necessary
    if official_hint_string:
        target_symbol = official_hint_string + " "
        if target_symbol in tmp_text:
            star_index = tmp_text.find(target_symbol)
            next_block_index = star_index + len(target_symbol)
            space_index = tmp_text.find(" ", next_block_index)
            next_block = tmp_text[next_block_index:space_index]
            if CONST_EXAMPLE_SYMBOL in next_block:
                official_hint_string += ' ' + next_block

    # Apply specific hint rules based on character count hints
    char_count_rules = [
        ("個半形英文大寫", 'A'),
        ("個英文大寫", 'A'),
        ("個半形英文小寫", 'a'),
        ("個英文小寫", 'a'),
        ("個英數半形字", r'[A-Za-z\d]')
    ]
    for target_symbol, char_type in char_count_rules:
        if not official_hint_string and target_symbol in tmp_text:
            star_index = tmp_text.find(target_symbol)
            space_index = tmp_text.find(" ", star_index)
            answer_char_count = tmp_text[star_index - 1:star_index]
            if answer_char_count.isnumeric():
                answer_char_count = chinese_numeric_to_int(answer_char_count)
                if answer_char_count is None:
                    answer_char_count = '0'
                official_hint_string_answer = char_type * int(answer_char_count)
            official_hint_string = tmp_text[star_index:space_index]

    # Format the answer from the extracted hint
    if official_hint_string_answer:
        my_answer_formatted = convert_string_to_pattern(official_hint_string_answer)

    # Remove question part from the options and replace the official hint string
    my_options = tmp_text.replace(my_question, "").replace(official_hint_string, "")

    # Use pattern to search for the answer within the options
    if my_answer_formatted:
        allow_delimiter_symbols = ")].: }"
        pattern = re.compile(my_answer_formatted)
        search_result = pattern.search(my_options)
        if search_result:
            span_start, span_end = search_result.span()
            maybe_delimiter = my_options[span_end:span_end + 1]
            if maybe_delimiter in allow_delimiter_symbols:
                my_answer_delimiter = maybe_delimiter

    if show_debug_message:
        print("my_answer_delimiter:", my_answer_delimiter)

    # Check if the answer delimiter is valid and extract the answers
    is_trim_quota = not check_answer_keep_symbol(tmp_text)
    return_list = []
    if my_answer_formatted:
        new_pattern = my_answer_formatted + ('\\' + my_answer_delimiter if my_answer_delimiter else '')
        return_list = re.findall(new_pattern, my_options)

        if len(return_list) == 1:
            return_list = re.findall(my_answer_formatted, my_options)

        if len(return_list) == 1:
            return_list = None

        # Clean delimiters from the answer list
        if return_list:
            if is_trim_quota and my_answer_delimiter:
                return_list = [answer.replace(my_answer_delimiter, '') for answer in return_list]

        if return_list is None:
            return_list = []

    return return_list, official_hint_string_answer


def format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text):
    tmp_text = captcha_text_div_text
    tmp_text = tmp_text.replace('  ', ' ')
    tmp_text = tmp_text.replace('：', ':')
    # for hint
    tmp_text = tmp_text.replace('*', '*')

    # stop word.
    tmp_text = tmp_text.replace('輸入法', '')
    tmp_text = tmp_text.replace('請問', '')
    tmp_text = tmp_text.replace('請將', '')
    tmp_text = tmp_text.replace('請在', '')
    tmp_text = tmp_text.replace('請以', '')
    tmp_text = tmp_text.replace('請回答', '')
    tmp_text = tmp_text.replace('請', '')

    # replace ex.
    tmp_text = tmp_text.replace('例如', CONST_EXAMPLE_SYMBOL)
    tmp_text = tmp_text.replace('如:', CONST_EXAMPLE_SYMBOL)
    tmp_text = tmp_text.replace('如為', CONST_EXAMPLE_SYMBOL + '為')

    tmp_text = tmp_text.replace('舉例', CONST_EXAMPLE_SYMBOL)
    if not CONST_EXAMPLE_SYMBOL in tmp_text:
        tmp_text = tmp_text.replace('例', CONST_EXAMPLE_SYMBOL)
    # important, maybe 例 & ex occurs at same time.
    tmp_text = tmp_text.replace('ex:', CONST_EXAMPLE_SYMBOL)
    tmp_text = tmp_text.replace('Ex:', CONST_EXAMPLE_SYMBOL)

    # 若你覺得
    # PS:這個，可能會造成更多問題，呵呵。
    SYMBOL_IF_LIST = ['假設', '如果', '若']
    for symbol_if in SYMBOL_IF_LIST:
        if symbol_if in tmp_text and '答案' in tmp_text:
            tmp_text = tmp_text.replace('覺得', '')
            tmp_text = tmp_text.replace('認為', '')
            tmp_text = tmp_text.replace(symbol_if + '你答案', CONST_EXAMPLE_SYMBOL + '答案')
            tmp_text = tmp_text.replace(symbol_if + '答案', CONST_EXAMPLE_SYMBOL + '答案')

    tmp_text = tmp_text.replace('填入', CONST_INPUT_SYMBOL)

    # tmp_text = tmp_text.replace('[','(')
    # tmp_text = tmp_text.replace(']',')')
    tmp_text = tmp_text.replace('？', '?')

    tmp_text = tmp_text.replace('（', '(')
    tmp_text = tmp_text.replace('）', ')')

    return tmp_text


def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n - r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def get_answer_list_by_question(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text):
    show_debug_message = True  # debug.
    show_debug_message = False  # online

    return_list = []

    tmp_text = format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)

    # guess answer list from multi-options: 【】() []
    if len(return_list) == 0:
        return_list = guess_answer_list_from_multi_options(tmp_text)
    if show_debug_message:
        print("captcha_text_div_text:", captcha_text_div_text)
        if len(return_list) > 0:
            print("found, guess_answer_list_from_multi_options:", return_list)

    offical_hint_string_anwser = ""
    if len(return_list) == 0:
        return_list, offical_hint_string_anwser = guess_answer_list_from_hint(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL,
                                                                              captcha_text_div_text)
    else:
        is_match_factorial = False
        mutiple = 0

        return_list_2, offical_hint_string_anwser = guess_answer_list_from_hint(CONST_EXAMPLE_SYMBOL,
                                                                                CONST_INPUT_SYMBOL,
                                                                                captcha_text_div_text)
        if return_list_2 is None:
            if len(offical_hint_string_anwser) >= 3:
                if len(return_list) >= 3:
                    mutiple = int(len(offical_hint_string_anwser) / len(return_list[0]))
                    if mutiple >= 3:
                        is_match_factorial = True

        if show_debug_message:
            print("mutiple:", mutiple)
            print("is_match_factorial:", is_match_factorial)
        if is_match_factorial:
            is_match_factorial = False
            order_string_list = ['排列', '排序', '依序', '順序', '遞增', '遞減', '升冪', '降冪', '新到舊', '舊到新', '小到大', '大到小', '高到低',
                                 '低到高']
            for order_string in order_string_list:
                if order_string in tmp_text:
                    is_match_factorial = True

        if is_match_factorial:
            new_array = permutations(return_list, mutiple)
            # print("new_array:", new_array)

            return_list = []
            for item_tuple in new_array:
                return_list.append(''.join(item_tuple))

        if show_debug_message:
            if len(return_list) > 0:
                print("found, guess_answer_list_from_hint:", return_list)

    if len(return_list) == 0:
        return_list = guess_answer_list_from_symbols(captcha_text_div_text)
        if show_debug_message:
            if len(return_list) > 0:
                print("found, guess_answer_list_from_symbols:", return_list)

    return return_list


def get_matched_blocks_by_keyword_item_set(config_dict, auto_select_mode, keyword_item_set, formated_area_list):
    show_debug_message = True  # debug.
    show_debug_message = False  # online

    if config_dict["advanced"]["verbose"]:
        show_debug_message = True

    matched_blocks = []
    for row in formated_area_list:
        row_text = ""
        row_html = ""
        try:
            # row_text = row.text
            row_html = row.get_attribute('innerHTML')
            row_text = remove_html_tags(row_html)
        except Exception as exc:
            if show_debug_message:
                print(exc)
            # error, exit loop
            break

        if len(row_text) > 0:
            if reset_row_text_if_match_keyword_exclude(config_dict, row_text):
                row_text = ""

        if len(row_text) > 0:
            # start to compare, normalize all.
            row_text = format_keyword_string(row_text)
            if show_debug_message:
                print("row_text:", row_text)

            is_match_all = False
            if ' ' in keyword_item_set:
                keyword_item_array = keyword_item_set.split(' ')
                is_match_all = True
                for keyword_item in keyword_item_array:
                    keyword_item = format_keyword_string(keyword_item)
                    if not keyword_item in row_text:
                        is_match_all = False
            else:
                exclude_item = format_keyword_string(keyword_item_set)
                if exclude_item in row_text:
                    is_match_all = True

            if is_match_all:
                matched_blocks.append(row)

                # only need first row.
                if auto_select_mode == CONST_FROM_TOP_TO_BOTTOM:
                    break
    return matched_blocks


def get_target_item_from_matched_list(matched_blocks, auto_select_mode):
    target_area = None
    if not matched_blocks is None:
        matched_blocks_count = len(matched_blocks)
        if matched_blocks_count > 0:
            target_row_index = 0

            if auto_select_mode == CONST_FROM_TOP_TO_BOTTOM:
                pass

            if auto_select_mode == CONST_FROM_BOTTOM_TO_TOP:
                target_row_index = matched_blocks_count - 1

            if auto_select_mode == CONST_RANDOM:
                if matched_blocks_count > 1:
                    target_row_index = random.randint(0, matched_blocks_count - 1)

            if auto_select_mode == CONST_CENTER:
                if matched_blocks_count > 2:
                    target_row_index = int(matched_blocks_count / 2)

            target_area = matched_blocks[target_row_index]
    return target_area


def get_matched_blocks_by_keyword(config_dict, auto_select_mode, keyword_string, formated_area_list):
    keyword_array = []
    try:
        keyword_array = json.loads("[" + keyword_string + "]")
    except Exception as exc:
        keyword_array = []

    matched_blocks = []
    for keyword_item_set in keyword_array:
        matched_blocks = get_matched_blocks_by_keyword_item_set(config_dict, auto_select_mode, keyword_item_set,
                                                                formated_area_list)
        if len(matched_blocks) > 0:
            break
    return matched_blocks


def is_row_match_keyword(keyword_string, row_text):
    # clean stop word.
    row_text = format_keyword_string(row_text)

    is_match_keyword = True
    if len(keyword_string) > 0 and len(row_text) > 0:
        is_match_keyword = False
        keyword_array = []
        try:
            keyword_array = json.loads("[" + keyword_string + "]")
        except Exception as exc:
            keyword_array = []
        for item_list in keyword_array:
            if len(item_list) > 0:
                if ' ' in item_list:
                    keyword_item_array = item_list.split(' ')
                    is_match_all_exclude = True
                    for each_item in keyword_item_array:
                        each_item = format_keyword_string(each_item)
                        if not each_item in row_text:
                            is_match_all_exclude = False
                    if is_match_all_exclude:
                        is_match_keyword = True
                else:
                    item_list = format_keyword_string(item_list)
                    if item_list in row_text:
                        is_match_keyword = True
            else:
                # match all.
                is_match_keyword = True
            if is_match_keyword:
                break
    return is_match_keyword


def reset_row_text_if_match_keyword_exclude(config_dict, row_text):
    area_keyword_exclude = config_dict["keyword_exclude"]
    return is_row_match_keyword(area_keyword_exclude, row_text)


def guess_tixcraft_question(driver, question_text):
    show_debug_message = True  # debug.
    show_debug_message = False  # online

    answer_list = []

    formated_html_text = ""
    if len(question_text) > 0:
        # format question text.
        formated_html_text = question_text
        formated_html_text = format_quota_string(formated_html_text)

        if '【' in formated_html_text and '】' in formated_html_text:
            # PS: 這個太容易沖突，因為問題類型太多，不能直接使用。
            # inferred_answer_string = find_between(formated_html_text, "【", "】")
            pass

    if show_debug_message:
        print("formated_html_text:", formated_html_text)

    # start to guess answer
    inferred_answer_string = None

    # 請輸入"YES"，代表您已詳閱且瞭解並同意。
    if inferred_answer_string is None:
        if '輸入"YES"' in formated_html_text:
            if '已詳閱' in formated_html_text or '請詳閱' in formated_html_text:
                if '同意' in formated_html_text:
                    inferred_answer_string = 'YES'

    # 購票前請詳閱注意事項，並於驗證碼欄位輸入【同意】繼續購票流程。
    if inferred_answer_string is None:
        if '驗證碼' in formated_html_text or '驗證欄位' in formated_html_text:
            if '已詳閱' in formated_html_text or '請詳閱' in formated_html_text:
                if '輸入【同意】' in formated_html_text:
                    inferred_answer_string = '同意'

    if inferred_answer_string is None:
        if len(question_text) > 0:
            answer_list = get_answer_list_from_question_string(None, question_text)
    else:
        answer_list = [answer_list]

    return answer_list


def get_answer_list_from_user_guess_string(config_dict, CONST_MAXBOT_ANSWER_ONLINE_FILE):
    local_array = []
    online_array = []

    user_guess_string = config_dict["advanced"]["user_guess_string"]
    if len(user_guess_string) > 0:
        user_guess_string = format_config_keyword_for_json(user_guess_string)
        try:
            local_array = json.loads("[" + user_guess_string + "]")
        except Exception as exc:
            local_array = []

    # load from internet.
    user_guess_string = ""
    if os.path.exists(CONST_MAXBOT_ANSWER_ONLINE_FILE):
        try:
            with open(CONST_MAXBOT_ANSWER_ONLINE_FILE, "r") as text_file:
                user_guess_string = text_file.readline()
        except Exception as e:
            pass

    if len(user_guess_string) > 0:
        user_guess_string = format_config_keyword_for_json(user_guess_string)
        try:
            online_array = json.loads("[" + user_guess_string + "]")
        except Exception as exc:
            online_array = []

    return local_array + online_array


def check_answer_keep_symbol(captcha_text_div_text):
    is_need_keep_symbol = False

    # format text
    keep_symbol_tmp = captcha_text_div_text
    keep_symbol_tmp = keep_symbol_tmp.replace('也', '須')
    keep_symbol_tmp = keep_symbol_tmp.replace('必須', '須')

    keep_symbol_tmp = keep_symbol_tmp.replace('全都', '都')
    keep_symbol_tmp = keep_symbol_tmp.replace('全部都', '都')

    keep_symbol_tmp = keep_symbol_tmp.replace('一致', '相同')
    keep_symbol_tmp = keep_symbol_tmp.replace('一樣', '相同')
    keep_symbol_tmp = keep_symbol_tmp.replace('相等', '相同')

    if '符號須都相同' in keep_symbol_tmp:
        is_need_keep_symbol = True

    if '符號都相同' in keep_symbol_tmp:
        is_need_keep_symbol = True

    if '符號須相同' in keep_symbol_tmp:
        is_need_keep_symbol = True

    # for: 大小寫含括號需一模一樣
    keep_symbol_tmp = keep_symbol_tmp.replace('含', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('和', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('與', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('還有', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('及', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('以及', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('需', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('必須', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('而且', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('且', '')
    keep_symbol_tmp = keep_symbol_tmp.replace('一模', '')
    # print("keep_symbol_tmp:", keep_symbol_tmp)
    if '大小寫括號相同' in keep_symbol_tmp:
        is_need_keep_symbol = True

    return is_need_keep_symbol


# PS: this is for selenium webdriver.
def kktix_get_web_datetime(registrationsNewApp_div):
    show_debug_message = True  # debug.
    show_debug_message = False  # online

    web_datetime = None

    is_found_web_datetime = False

    el_web_datetime_list = None
    if not registrationsNewApp_div is None:
        try:
            el_web_datetime_list = registrationsNewApp_div.find_elements(By.TAG_NAME, 'td')
        except Exception as exc:
            if show_debug_message:
                print("find td.ng-binding Exception")
                print(exc)
            pass
        # print("is_found_web_datetime", is_found_web_datetime)

    if not el_web_datetime_list is None:
        el_web_datetime_list_count = len(el_web_datetime_list)
        if el_web_datetime_list_count > 0:
            el_web_datetime = None
            for el_web_datetime in el_web_datetime_list:
                el_web_datetime_text = None
                try:
                    el_web_datetime_text = el_web_datetime.text
                    if show_debug_message:
                        print("el_web_datetime_text:", el_web_datetime_text)
                except Exception as exc:
                    if show_debug_message:
                        print('parse web datetime fail:')
                        print(exc)
                    pass

                if not el_web_datetime_text is None:
                    if len(el_web_datetime_text) > 0:
                        now = datetime.now()
                        # print("now:", now)
                        for guess_year in range(now.year, now.year + 3):
                            current_year = str(guess_year)
                            if current_year in el_web_datetime_text:
                                if '/' in el_web_datetime_text:
                                    web_datetime = el_web_datetime_text
                                    is_found_web_datetime = True
                                    break
                        if is_found_web_datetime:
                            break
    else:
        print("find td.ng-binding fail")

    if show_debug_message:
        print('is_found_web_datetime:', is_found_web_datetime)
        print('web_datetime:', web_datetime)

    return web_datetime


def get_answer_string_from_web_date(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, registrationsNewApp_div,
                                    captcha_text_div_text):
    show_debug_message = True  # debug.
    show_debug_message = False  # online

    inferred_answer_string = None

    is_need_parse_web_datetime = False
    # '半形阿拉伯數字' & '半形數字'
    if '半形' in captcha_text_div_text and '字' in captcha_text_div_text:
        if '演出日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '活動日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '表演日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '開始日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '演唱會日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '展覽日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
        if '音樂會日期' in captcha_text_div_text:
            is_need_parse_web_datetime = True
    if 'the date of the show you purchased' in captcha_text_div_text:
        is_need_parse_web_datetime = True

    if show_debug_message:
        print("is_need_parse_web_datetime:", is_need_parse_web_datetime)

    if is_need_parse_web_datetime:
        web_datetime = kktix_get_web_datetime(registrationsNewApp_div)
        if not web_datetime is None:
            if show_debug_message:
                print("web_datetime:", web_datetime)

            captcha_text_formatted = format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL,
                                                            captcha_text_div_text)
            if show_debug_message:
                print("captcha_text_formatted", captcha_text_formatted)

            my_datetime_foramted = None

            # MMDD
            if my_datetime_foramted is None:
                if '4位半形' in captcha_text_formatted:
                    my_datetime_foramted = "%m%d"

            # for "如為2月30日，請輸入0230"
            if my_datetime_foramted is None:
                right_part = ""
                if CONST_EXAMPLE_SYMBOL in captcha_text_formatted:
                    right_part = captcha_text_formatted.split(CONST_EXAMPLE_SYMBOL)[1]

                if CONST_INPUT_SYMBOL in right_part:
                    right_part = right_part.split(CONST_INPUT_SYMBOL)[1]
                    number_text = find_continuous_number(right_part)

                    my_anwser_formated = convert_string_to_pattern(number_text, dynamic_length=False)
                    if my_anwser_formated == "[\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d]":
                        my_datetime_foramted = "%Y%m%d"
                    if my_anwser_formated == "[\\d][\\d][\\d][\\d]":
                        my_datetime_foramted = "%m%d"
                    # print("my_datetime_foramted:", my_datetime_foramted)

            if show_debug_message:
                print("my_datetime_foramted", my_datetime_foramted)

            if my_datetime_foramted is None:
                now = datetime.now()
                for guess_year in range(now.year - 4, now.year + 2):
                    current_year = str(guess_year)
                    if current_year in captcha_text_formatted:
                        my_hint_index = captcha_text_formatted.find(current_year)
                        my_hint_anwser = captcha_text_formatted[my_hint_index:]
                        # print("my_hint_anwser:", my_hint_anwser)
                        # get after.
                        my_delimitor_symbol = CONST_EXAMPLE_SYMBOL
                        if my_delimitor_symbol in my_hint_anwser:
                            my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                            my_hint_anwser = my_hint_anwser[my_delimitor_index + len(my_delimitor_symbol):]
                        # print("my_hint_anwser:", my_hint_anwser)
                        # get before.
                        my_delimitor_symbol = '，'
                        if my_delimitor_symbol in my_hint_anwser:
                            my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                            my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                        my_delimitor_symbol = '。'
                        if my_delimitor_symbol in my_hint_anwser:
                            my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                            my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                        # PS: space may not is delimitor...
                        my_delimitor_symbol = ' '
                        if my_delimitor_symbol in my_hint_anwser:
                            my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                            my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                        # remove last char.
                        remove_last_char_list = [')', '(', '.', '。', '）', '（', '[', ']']
                        for check_char in remove_last_char_list:
                            if my_hint_anwser[-1:] == check_char:
                                my_hint_anwser = my_hint_anwser[:-1]

                        my_anwser_formated = convert_string_to_pattern(my_hint_anwser, dynamic_length=False)
                        if my_anwser_formated == "[\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d]":
                            my_datetime_foramted = "%Y%m%d"
                        if my_anwser_formated == "[\\d][\\d][\\d][\\d]/[\\d][\\d]/[\\d][\\d]":
                            my_datetime_foramted = "%Y/%m/%d"

                        if show_debug_message:
                            print("my_hint_anwser:", my_hint_anwser)
                            print("my_anwser_formated:", my_anwser_formated)
                            print("my_datetime_foramted:", my_datetime_foramted)
                        break

            if not my_datetime_foramted is None:
                my_delimitor_symbol = ' '
                if my_delimitor_symbol in web_datetime:
                    web_datetime = web_datetime[:web_datetime.find(my_delimitor_symbol)]
                date_time = datetime.strptime(web_datetime, "%Y/%m/%d")
                if show_debug_message:
                    print("our web date_time:", date_time)
                ans = None
                try:
                    if not date_time is None:
                        ans = date_time.strftime(my_datetime_foramted)
                except Exception as exc:
                    pass
                inferred_answer_string = ans
                if show_debug_message:
                    print("web date_time anwser:", ans)

    return inferred_answer_string


def get_answer_string_from_web_time(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, registrationsNewApp_div,
                                    captcha_text_div_text):
    show_debug_message = True  # debug.
    show_debug_message = False  # online

    inferred_answer_string = None

    # parse '演出時間'
    is_need_parse_web_time = False
    if '半形' in captcha_text_div_text:
        if '演出時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '表演時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '開始時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '演唱會時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '展覽時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if '音樂會時間' in captcha_text_div_text:
            is_need_parse_web_time = True
        if 'the time of the show you purchased' in captcha_text_div_text:
            is_need_parse_web_time = True

    # print("is_need_parse_web_time", is_need_parse_web_time)
    if is_need_parse_web_time:
        web_datetime = None
        if not registrationsNewApp_div is None:
            web_datetime = kktix_get_web_datetime(registrationsNewApp_div)
        if not web_datetime is None:
            tmp_text = format_question_string(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)

            my_datetime_foramted = None

            if my_datetime_foramted is None:
                my_hint_anwser = tmp_text

                my_delimitor_symbol = CONST_EXAMPLE_SYMBOL
                if my_delimitor_symbol in my_hint_anwser:
                    my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                    my_hint_anwser = my_hint_anwser[my_delimitor_index + len(my_delimitor_symbol):]
                # print("my_hint_anwser:", my_hint_anwser)
                # get before.
                my_delimitor_symbol = '，'
                if my_delimitor_symbol in my_hint_anwser:
                    my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                    my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                my_delimitor_symbol = '。'
                if my_delimitor_symbol in my_hint_anwser:
                    my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                    my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                # PS: space may not is delimitor...
                my_delimitor_symbol = ' '
                if my_delimitor_symbol in my_hint_anwser:
                    my_delimitor_index = my_hint_anwser.find(my_delimitor_symbol)
                    my_hint_anwser = my_hint_anwser[:my_delimitor_index]
                my_anwser_formated = convert_string_to_pattern(my_hint_anwser, dynamic_length=False)
                # print("my_hint_anwser:", my_hint_anwser)
                # print("my_anwser_formated:", my_anwser_formated)
                if my_anwser_formated == "[\\d][\\d][\\d][\\d]":
                    my_datetime_foramted = "%H%M"
                    if '12小時' in tmp_text:
                        my_datetime_foramted = "%I%M"

                if my_anwser_formated == "[\\d][\\d]:[\\d][\\d]":
                    my_datetime_foramted = "%H:%M"
                    if '12小時' in tmp_text:
                        my_datetime_foramted = "%I:%M"

            if not my_datetime_foramted is None:
                date_delimitor_symbol = '('
                if date_delimitor_symbol in web_datetime:
                    date_delimitor_symbol_index = web_datetime.find(date_delimitor_symbol)
                    if date_delimitor_symbol_index > 8:
                        web_datetime = web_datetime[:date_delimitor_symbol_index - 1]
                date_time = datetime.strptime(web_datetime, "%Y/%m/%d %H:%M")
                # print("date_time:", date_time)
                ans = None
                try:
                    ans = date_time.strftime(my_datetime_foramted)
                except Exception as exc:
                    pass
                inferred_answer_string = ans
                # print("my_anwser:", ans)

    return inferred_answer_string


def get_answer_list_from_question_string(registrationsNewApp_div, captcha_text_div_text):
    show_debug_message = True  # debug.
    show_debug_message = False  # online

    inferred_answer_string = None
    answer_list = []

    CONST_EXAMPLE_SYMBOL = "範例"
    CONST_INPUT_SYMBOL = "輸入"

    if captcha_text_div_text is None:
        captcha_text_div_text = ""

    # 請在下方空白處輸入引號內文字：
    # 請回答下列問題,請在下方空格輸入DELIGHT（請以半形輸入法作答，大小寫需要一模一樣）
    if inferred_answer_string is None:
        is_use_quota_message = False
        if "「" in captcha_text_div_text and "」" in captcha_text_div_text:
            # test for rule#1, it's seem very easy conflict...
            match_quota_text_items = ["空白", "輸入", "引號", "文字"]
            is_match_quota_text = True
            for each_quota_text in match_quota_text_items:
                if not each_quota_text in captcha_text_div_text:
                    is_match_quota_text = False
            if is_match_quota_text:
                is_use_quota_message = True
        # print("is_use_quota_message:" , is_use_quota_message)
        if is_use_quota_message:
            temp_answer = find_between(captcha_text_div_text, "「", "」")
            temp_answer = temp_answer.strip()
            if len(temp_answer) > 0:
                inferred_answer_string = temp_answer
            # print("find captcha text:" , inferred_answer_string)

    # 請在下方空白處輸入括號內數字
    if inferred_answer_string is None:
        formated_html_text = captcha_text_div_text.strip()
        formated_html_text = format_quota_string(formated_html_text)
        formated_html_text = formated_html_text.replace('請輸入', '輸入')

        formated_html_text = formated_html_text.replace('的', '')
        formated_html_text = formated_html_text.replace('之內', '內')
        formated_html_text = formated_html_text.replace('之中', '中')

        formated_html_text = formated_html_text.replace('括弧', '括號')
        formated_html_text = formated_html_text.replace('引號', '括號')

        formated_html_text = formated_html_text.replace('括號中', '括號內')

        formated_html_text = formated_html_text.replace('數字', '文字')

        is_match_input_quota_text = False
        if len(formated_html_text) <= 30:
            if not '\n' in formated_html_text:
                if '【' in formated_html_text and '】' in formated_html_text:
                    is_match_input_quota_text = True

        # check target text terms.
        if is_match_input_quota_text:
            target_text_list = ["輸入", "括號", "文字"]
            for item in target_text_list:
                if not item in formated_html_text:
                    is_match_input_quota_text = False
                    break

        if is_match_input_quota_text:
            temp_answer = find_between(formated_html_text, "【", "】")
            temp_answer = temp_answer.strip()
            if len(temp_answer) > 0:
                temp_answer = temp_answer.replace(' ', '')

                # check raw question.
                if '數字' in captcha_text_div_text:
                    temp_answer = normalize_chinese_numeric(temp_answer)

                inferred_answer_string = temp_answer

    # 請將括弧內文字轉換為阿拉伯數字
    if inferred_answer_string is None:
        formated_html_text = captcha_text_div_text.strip()
        formated_html_text = format_quota_string(formated_html_text)
        formated_html_text = formated_html_text.replace('請輸入', '輸入')

        formated_html_text = formated_html_text.replace('的', '')
        formated_html_text = formated_html_text.replace('之內', '內')
        formated_html_text = formated_html_text.replace('之中', '中')

        formated_html_text = formated_html_text.replace('括弧', '括號')
        formated_html_text = formated_html_text.replace('引號', '括號')

        formated_html_text = formated_html_text.replace('括號中', '括號內')

        formated_html_text = formated_html_text.replace('修改', '轉換')
        formated_html_text = formated_html_text.replace('調整', '轉換')
        formated_html_text = formated_html_text.replace('改變', '轉換')
        formated_html_text = formated_html_text.replace('改為', '轉換')
        formated_html_text = formated_html_text.replace('置換', '轉換')
        formated_html_text = formated_html_text.replace('換成', '轉換')

        is_match_input_quota_text = False
        if len(formated_html_text) <= 30:
            print("formated_html_text:", formated_html_text)
            if not '\n' in formated_html_text:
                if '【' in formated_html_text and '】' in formated_html_text:
                    is_match_input_quota_text = True

        # check target text terms.
        if is_match_input_quota_text:
            target_text_list = ["轉換", "數字", "文字"]
            for item in target_text_list:
                if not item in formated_html_text:
                    is_match_input_quota_text = False
                    break

        if is_match_input_quota_text:
            temp_answer = find_between(formated_html_text, "【", "】")
            temp_answer = temp_answer.strip()
            if len(temp_answer) > 0:
                temp_answer = temp_answer.replace(' ', '')
                temp_answer = normalize_chinese_numeric(temp_answer)
                inferred_answer_string = temp_answer

    if inferred_answer_string is None:
        is_use_quota_message = False
        if "【" in captcha_text_div_text and "】" in captcha_text_div_text:
            if '下' in captcha_text_div_text and '空' in captcha_text_div_text and CONST_INPUT_SYMBOL in captcha_text_div_text and '引號' in captcha_text_div_text and '字' in captcha_text_div_text:
                is_use_quota_message = True
            if '半形' in captcha_text_div_text and CONST_INPUT_SYMBOL in captcha_text_div_text and '引號' in captcha_text_div_text and '字' in captcha_text_div_text:
                is_use_quota_message = True
        # print("is_use_quota_message:" , is_use_quota_message)
        if is_use_quota_message:
            inferred_answer_string = find_between(captcha_text_div_text, "【", "】")
            inferred_answer_string = inferred_answer_string.strip()
            # print("find captcha text:" , inferred_answer_string)

    # parse '演出日期'
    if inferred_answer_string is None:
        inferred_answer_string = get_answer_string_from_web_date(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL,
                                                                 registrationsNewApp_div, captcha_text_div_text)

    # parse '演出時間'
    if inferred_answer_string is None:
        inferred_answer_string = get_answer_string_from_web_time(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL,
                                                                 registrationsNewApp_div, captcha_text_div_text)

    # name of event.
    if inferred_answer_string is None:
        if "name of event" in captcha_text_div_text:
            if '(' in captcha_text_div_text and ')' in captcha_text_div_text and 'ans:' in captcha_text_div_text.lower():
                target_symbol = "("
                star_index = captcha_text_div_text.find(target_symbol)
                target_symbol = ":"
                star_index = captcha_text_div_text.find(target_symbol, star_index)
                target_symbol = ")"
                end_index = captcha_text_div_text.find(target_symbol, star_index)
                inferred_answer_string = captcha_text_div_text[star_index + 1:end_index]
                # print("inferred_answer_string:", inferred_answer_string)

    # 二題式，組合問題。
    is_combine_two_question = False
    if "第一題" in captcha_text_div_text and "第二題" in captcha_text_div_text:
        is_combine_two_question = True
    if "Q1." in captcha_text_div_text and "Q2." in captcha_text_div_text:
        if "二題" in captcha_text_div_text:
            is_combine_two_question = True
        if "2題" in captcha_text_div_text:
            is_combine_two_question = True
    if "Q1:" in captcha_text_div_text and "Q2:" in captcha_text_div_text:
        if "二題" in captcha_text_div_text:
            is_combine_two_question = True
        if "2題" in captcha_text_div_text:
            is_combine_two_question = True
    if "Q1 " in captcha_text_div_text and "Q2 " in captcha_text_div_text:
        if "二題" in captcha_text_div_text:
            is_combine_two_question = True
        if "2題" in captcha_text_div_text:
            is_combine_two_question = True
    if is_combine_two_question:
        inferred_answer_string = None
    # print("is_combine_two_question:", is_combine_two_question)

    # still no answer.
    if inferred_answer_string is None:
        if not is_combine_two_question:
            answer_list = get_answer_list_by_question(CONST_EXAMPLE_SYMBOL, CONST_INPUT_SYMBOL, captcha_text_div_text)
            if show_debug_message:
                print("guess answer list:", answer_list)
        else:
            if show_debug_message:
                print("skip to guess answer because of combine question...")

    else:
        if show_debug_message:
            print("got an inferred_answer_string:", inferred_answer_string)
        answer_list = [inferred_answer_string]

    return answer_list


def kktix_get_registerStatus(event_code):
    html_result = None

    url = "https://kktix.com/g/events/%s/register_info" % (event_code)
    # print('event_code:',event_code)
    # print("url:", url)

    headers = {"Accept-Language": "zh-TW,zh;q=0.5", 'User-Agent': USER_AGENT}
    try:
        html_result = requests.get(url, headers=headers, timeout=0.7, allow_redirects=False)
    except Exception as exc:
        html_result = None
        print("send reg_info request fail:")
        print(exc)

    registerStatus = ""
    if not html_result is None:
        status_code = html_result.status_code
        # print("status_code:",status_code)
        if status_code == 200:
            html_text = html_result.text
            # print("html_text:", html_text)
            try:
                jsLoads = json.loads(html_text)
                if 'inventory' in jsLoads:
                    if 'registerStatus' in jsLoads['inventory']:
                        registerStatus = jsLoads['inventory']['registerStatus']
            except Exception as exc:
                print("load reg_info json fail:")
                print(exc)
                pass

    # print("registerStatus:", registerStatus)
    return registerStatus


def kktix_get_event_code(url):
    event_code = ""
    if '/registrations/new' in url:
        prefix_list = ['.com/events/', '.cc/events/']
        postfix = '/registrations/new'

        for prefix in prefix_list:
            event_code = find_between(url, prefix, postfix)
            if len(event_code) > 0:
                break

    # print('event_code:',event_code)
    return event_code


def get_kktix_status_by_url(url):
    registerStatus = ""
    if len(url) > 0:
        event_code = kktix_get_event_code(url)
        # print(event_code)
        if len(event_code) > 0:
            registerStatus = kktix_get_registerStatus(event_code)
            # print(registerStatus)
    return registerStatus
