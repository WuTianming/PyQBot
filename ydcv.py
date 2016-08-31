#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
from argparse import ArgumentParser
from subprocess import check_output
from urllib.parse import quote
from urllib.request import urlopen
from time import sleep
import json
import re
import sys


API = "API HERE"
API_KEY = "API_KEY HERE"


def print_explanation(data):
    result = ''
    _d = data
    has_result = False

    query = _d['query']
    result += '有道翻译：' + query

    if 'basic' in _d:
        has_result = True
        _b = _d['basic']

        if 'uk-phonetic' in _b and 'us-phonetic' in _b:
            result += '\n英式读音：' + _b['uk-phonetic'] + '\n美式读音：' + _b['us-phonetic']
        elif 'phonetic' in _b:
            result += '\n读音：' + _b['phonetic']

        if 'explains' in _b:
            result += '\n单词解释：'
            for item in _b['explains']:
                result += '\n    * ' + item

    elif 'translation' in _d:
        has_result = True
        result += '\n翻译：'
        for item in _d['translation']:
            result += '\n    * ' + item

    if not has_result:
        result += '\n无相关内容'

    return result


def lookup_word(word):
    word = quote(word)
    try:
        data = urlopen(
            "http://fanyi.youdao.com/openapi.do?keyfrom={0}&"
            "key={1}&type=data&doctype=json&version=1.2&q={2}"
            .format(API, API_KEY, word)).read().decode("utf-8")
    except IOError:
        print("Network is unavailable")
    else:
        return print_explanation(json.loads(data))
