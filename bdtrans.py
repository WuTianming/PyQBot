#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
from argparse import ArgumentParser
from subprocess import check_output
from urllib.parse import quote
from urllib.request import urlopen
from time import sleep
from hashlib import md5
import random
import json
import re
import sys


APPID = "APPID HERE"
API_KEY = "API_KEY HERE"


def has_chinese_charactar(content):
    try:
        iconvcontent = str(content)
        zhPattern = re.compile('[\u4e00-\u9fa5]+')
        match = zhPattern.search(iconvcontent)
        res = False
        if match:
            res = True
        return res
    except:
        return True


def print_explanation(data):
    result = ''

    result = '百度翻译：'
    for i in range(0, len(data['trans_result'])):
        result += data['trans_result'][i]['src'] + '\n'

    result += '来源语言：' + data['from']
    result += '\n目标语言：' + data['to']

    result += '\n翻译结果：'
    for i in range(0, len(data['trans_result'])):
        result += '\n    * ' + data['trans_result'][i]['dst']

    return result


def lookup_word(word, fromLang = None, toLang = None):
    try:
        if fromLang == None and toLang == None:
            if has_chinese_charactar(word):
                fromLang = 'zh'
                toLang = 'en'
            else:
                fromLang = 'auto'
                toLang = 'zh'
        salt = random.randint(32768, 65536)
        sign = APPID + word + str(salt) + API_KEY
        m = md5(sign.encode())
        sign = m.hexdigest()
        data = urlopen(
            "http://api.fanyi.baidu.com/api/trans/vip/translate/?appid={0}&"
            "q={1}&from={2}&to={3}&salt={4}&sign={5}"
            .format(APPID, quote(word), fromLang, toLang, salt, sign)).read().decode("utf-8")
    except IOError:
        print("Network is unavailable")
    else:
        return print_explanation(json.loads(data))
