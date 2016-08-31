#!/usr/bin/env python3

import re
import json
import sys
import collections
import time
import mlogger as log
import ydcv
import bdtrans
from wolfram import wolfram
from mogic import jiangzemin
from tuling import tuling
from xml.etree import ElementTree as etree
from urllib import request, parse
from qqrobot import QQClient, QQHandler

histMsg = {}
lastSay = {}
debug = False

def getHitokoto():
    f = request.urlopen('http://api.lwl12.com/hitokoto/main/get')
    return f.read().decode('utf-8')

class MsgHandler(QQHandler):
    def send_msg_group(self, group, init, msg, logTag):
        global histMsg
        global lastSay
        sendMsg = init
        for line in msg.split('\n'):
            if len(line) >= 300:
                self.send_group_message(group['gid'], sendMsg)
                log.i(logTag, 'response: ' + sendMsg)
                histMsg[group['name']] = sendMsg
                lastSay[group['name']] = '我'
                time.sleep(0.5)
                sendMsg = init
            sendMsg += '\n' + line
            if len(sendMsg) >= 300:
                self.send_group_message(group['gid'], sendMsg)
                log.i(logTag, 'response: ' + sendMsg)
                histMsg[group['name']] = sendMsg
                lastSay[group['name']] = '我'
                time.sleep(0.5)
                sendMsg = init
        if sendMsg != init:
            self.send_group_message(group['gid'], sendMsg)
            log.i(logTag, 'response: ' + sendMsg)
            histMsg[group['name']] = sendMsg
            lastSay[group['name']] = '我'
            time.sleep(0.5)

    def on_group_message(self, gid, uin, msg):
        global histMsg
        global lastSay
        hist = ''

        group = self.get_group_info(gid)
        user = group['members'][uin]
        log.i('QQBot', user['nick'] + '@' + group['name'] + ': ' + msg)

        if group['name'] in histMsg.keys():
            hist = histMsg[group['name']]
            if msg[0] == '^':
                msg = msg[1:] + ' ' + hist
        else:
            hist = ''
        histMsg[group['name']] = msg

        if group['name'] in lastSay.keys():
            lsay = lastSay[group['name']]
        else:
            lsay = ''
        lastSay[group['name']] = user['nick']

        if debug == True:
            if group['name'] != 'wtmbot':
                return

        if msg[0:3].lower() == 'wa ':
            msg = msg[3:]
            rst = w.search(msg)
            reMsg = user['nick'] + '：'
            # print(rst)
            if rst == {}:
                reMsg += '好像Wolfram无法解释您的请求，请尝试换种说法。请不要刷屏哦！\nWolframAlpha返回数据为：' + str(rst)
            else:
                for resultItem in rst:
                    if len(resultItem) >= 300:
                        self.send_group_message(gid, reMsg)
                        log.i('Wolfram', 'response: ' + reMsg)
                        histMsg[group['name']] = reMsg
                        lastSay[group['name']] = '我'
                        time.sleep(0.5)
                        reMsg = user['nick'] + '：'
                    reMsg += '\n----' + resultItem + '----\n' + rst[resultItem]
                    if len(reMsg) >= 300:
                        self.send_group_message(gid, reMsg)
                        log.i('Wolfram', 'response: ' + reMsg)
                        histMsg[group['name']] = reMsg
                        lastSay[group['name']] = '我'
                        time.sleep(0.5)
                        reMsg = user['nick'] + '：'
            if reMsg != user['nick'] + '：':
                self.send_group_message(gid, reMsg)
                log.i('Wolfram', 'response: ' + reMsg)
                histMsg[group['name']] = reMsg
                lastSay[group['name']] = '我'

        elif msg[0:7].lower() == 'wtmbot ':
            msg = msg[7:]
            reMsg = user['nick'] + '：' + t.response(msg, uin)
            self.send_group_message(gid, reMsg)
            log.i('Tuling', 'response: ' + reMsg)
            histMsg[group['name']] = reMsg
            lastSay[group['name']] = '我'

        elif msg[0:4].lower() == 'ping':
            reMsg = user['nick'] + '：Pong!'
            self.send_group_message(gid, reMsg)
            log.i('PingPong', 'response: ' + reMsg)
            histMsg[group['name']] = reMsg
            lastSay[group['name']] = '我'

        elif msg[0:5].lower() == 'ydfy ':
            msg = msg[5:]
            # reMsg = user['nick'] + '：\n' + ydcv.lookup_word(msg)
            # self.send_group_message(gid, reMsg)
            # log.i('YDDict', 'response: ' + reMsg)
            # histMsg[group['name']] = reMsg
            self.send_msg_group(group, user['nick'] + '：', ydcv.lookup_word(msg), 'YDDict')

        elif msg[0:5].lower() == 'bdfy ':
            msg = msg[5:]
            # reMsg = user['nick'] + '：\n' + bdtrans.lookup_word(msg)
            # self.send_group_message(gid, reMsg)
            # log.i('BDTrans', 'response: ' + reMsg)
            # histMsg[group['name']] = reMsg
            self.send_msg_group(group, user['nick'] + '：', bdtrans.lookup_word(msg), 'BDTrans')

        elif msg[0:3].lower() == 'fy ':
            msg = msg[3:]
            fromLang = msg.split(' ')[0]
            toLang = msg.split(' ')[1]
            msg = ' '.join(msg.split(' ')[2:])
            # reMsg = user['nick'] + '：\n' + bdtrans.lookup_word(msg, fromLang, toLang)
            # self.send_group_message(gid, reMsg)
            # log.i('BDTrans', 'response: ' + reMsg)
            # histMsg[group['name']] = reMsg
            self.send_msg_group(group, user['nick'] + '：', bdtrans.lookup_word(msg, fromLang, toLang), 'BDTrans')

        elif msg[0:2] == '一言':
            cnt = 1
            msg = msg[2:]
            try:
                cnt = int(msg)
            except ValueError as e:
                if msg == '':
                    cnt = 1
                else:
                    cnt = 0
            for i in range(0, cnt):
                reMsg = getHitokoto()
                self.send_group_message(gid, reMsg)
                log.i('Hitokoto', 'response: ' + reMsg)
                histMsg[group['name']] = reMsg
                lastSay[group['name']] = '我'
                time.sleep(0.5)

        elif msg.lower() == 'help':
            reMsg = '----wtmbot帮助手册----\n→help\n    * 显示此帮助信息\n→wtmbot [要说的话]\n    * 与很傻的人工智能进行对话\n→wa [查询内容]\n    * 查询Wolfram|Alpha\n→ydfy [翻译内容]\n    * 有道中英翻译\n→bdfy [翻译内容]\n    * 百度翻译，中文翻译为英文，外文自动检测语言翻译成中文\n→fy [来源语言] [目标语言] [翻译内容]\n    * 指定语言进行百度翻译，来源语言可为auto，表示自动识别\n→一言 [（可选）条数]\n    * 返回指定条数的一言语录；若不指定条数，默认返回一条\n→s/[替换前]/[替换后]\n    * 这是一条正则表达式替代命令，将把你的上一条信息中的“[替换前]”替换为“[替换后]”\n→^[指令]\n    * 将上一条信息作为[指令]的参数'
            self.send_group_message(gid, reMsg)
            log.i('Manual', 'response: ' + reMsg)
            histMsg[group['name']] = reMsg
            lastSay[group['name']] = '我'

        elif msg[0:2] == 's/':
            cmd = re.match('s/([^/]+)/([^/]*)/?', msg)
            if cmd:
                try:
                    (afterRep, repCnt) = re.subn(cmd.group(1), cmd.group(2), hist)
                except Exception as e:
                    self.send_group_message(gid, user['nick'] + '：正则表达式配对失败！')
                    log.i('Sedbot', 'response: ' + user['nick'] + '：正则表达式配对失败！')

                if repCnt > 0:
                    if lsay == user['nick']:
                        reMsg = '{0}原本想说的是“{1}”'.format(user['nick'], afterRep)
                    else:
                        reMsg = '{0}认为{1}应该说“{2}”才对'.format(user['nick'], lsay, afterRep)
                    self.send_group_message(gid, reMsg)
                    log.i('Sedbot', 'response: ' + reMsg)
                    histMsg[group['name']] = reMsg
                    lastSay[group['name']] = '我'
                else:
                    self.send_group_message(gid, user['nick'] + '：正则表达式配对失败！')
                    log.i('Sedbot', 'response: ' + user['nick'] + '：正则表达式配对失败！')

        elif zemin.getMogic(msg) != False:
            reMsg = zemin.getMogic(msg)
            self.send_group_message(gid, reMsg)
            log.i('Mogic', 'response: ' + reMsg)
            histMsg[group['name']] = reMsg
            lastSay[group['name']] = '我'

if __name__ == "__main__":
    if sys.argv[-1] == 'debug':
        log.w('DEBUG', 'You are now running in DEBUG mode.')
        debug = True
    w = wolfram('APIKEY HERE')
    t = tuling('APIKEY HERE')
    zemin = jiangzemin()
    a = QQClient()
    h = MsgHandler()
    # a.QR_veri()
    # a.login()
    # a.save_veri()
    a.load_veri(sys.argv[1])
    a.login(get_info=False)
    a.add_handler(h)
    a.listen(join=True)
