#!/usr/bin/env python3

import json
import sys
import collections
import time
import mlogger as log
from wolfram import wolfram
from tuling import tuling
from xml.etree import ElementTree as etree
from urllib import request, parse
from qqrobot import QQClient, QQHandler

class MsgHandler(QQHandler):
    def on_group_message(self, gid, uin, msg):
        group = self.get_group_info(gid)
        user = group['members'][uin]
        log.i('QQBot', user['nick'] + '@' + group['name'] + ': ' + msg)
        if msg[0:3].lower() == 'wa ':
            msg = msg[3:]
            rst = w.search(msg)
            reMsg = user['nick'] + '：'
            # print(rst)
            if rst == {}:
                reMsg += '好像Wolfram无法解释您的请求，请尝试换种说法。请不要刷屏哦！\nWolframAlpha返回数据为：' + str(rst)
            else:
                for resultItem in rst:
                    if len(rst) >= 300:
                        self.send_group_message(gid, reMsg)
                        log.i('WABot', 'response: ' + reMsg)
                        time.sleep(0.5)
                        reMsg = user['nick'] + '：'
                    reMsg += '\n----' + resultItem + '----\n' + rst[resultItem]
                    if len(reMsg) >= 300:
                        self.send_group_message(gid, reMsg)
                        log.i('Wolfram', 'response: ' + reMsg)
                        time.sleep(0.5)
                        reMsg = user['nick'] + '：'
            if reMsg != user['nick'] + '：':
                self.send_group_message(gid, reMsg)
                log.i('Wolfram', 'response: ' + reMsg)
        elif msg[0:7].lower() == 'wtmbot ':
            msg = msg[7:]
            reMsg = user['nick'] + '：' + t.response(msg, uin)
            self.send_group_message(gid, reMsg)
            log.i('Tuling', 'response: ' + reMsg)
        elif msg[0:4].lower() == 'ping':
            reMsg = user['nick'] + '：Pong!'
            self.send_group_message(gid, reMsg)
            log.i('PingPong', 'response: ' + reMsg)

if __name__ == "__main__":
    w = wolfram('XXXXXX-XXXXXXXXXX')
    t = tuling('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    a = QQClient()
    h = MsgHandler()
    # a.QR_veri()
    # a.login()
    # a.save_veri()
    a.load_veri(sys.argv[1])
    a.login(get_info=False)
    a.add_handler(h)
    a.listen(join=True)
