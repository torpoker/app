import json
import base64
import binascii
import re


def resp_header_parse(resp_bytes: bytes, do_return: bool = False, captcha: bool = False):
    """
    receives headers response in bytes and parse captcha or content using 'ast' and returns the dict to caller function
    :param resp_bytes:
    :param do_return: True to return response (json), pass this as False
    :param captcha: True to return captcha base64 string, else False
    :return:
    """
    if resp_bytes is None:
        return '', None
    header_part = ''
    res_string = resp_bytes.decode('utf-8', errors='ignore')
    if '{' in res_string:
        string_json = res_string.split('\r\n\r\n')[-1]
        header_part = res_string[:res_string.index('{')]
        eval_json = json.loads(string_json)
        if 'error' in eval_json:
            return header_part, None
        if do_return:
            header_part = res_string[:res_string.index('{')]
            return header_part, eval_json
        # this is for captcha base64 string decoding
        if captcha:
            try:
                data = base64.b64decode(eval_json['captcha'], validate=True)
            except binascii.Error:  # for incorrect base64 string
                return header_part, None
            return header_part, data
    return header_part, None


def header_to_json(header_string):
    reg_pattern = "(.+)\:\ (.+?)\;"
    match_list = re.findall(reg_pattern, header_string, re.M)
    header_dict = {}
    if match_list:
        for item in match_list:
            if item[0] == "Set-Cookie":
                cookie_string = item[1]
                header_dict['Cookie'] = cookie_string
            else:
                header_dict[item[0]] = item[1]

    return header_dict
