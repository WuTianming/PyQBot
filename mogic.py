#!/usr/bin/env python3

class jiangzemin(object):
    def __init__(self):
        self.resultDict = {
            '苟': '利',
            '利': '国',
            '国': '家',
            '家': '生',
            '生': '死',
            '死': '以',
            '以': '岂',
            '岂': '因',
            '因': '祸',
            '祸': '福',
            '福': '避',
            '避': '趋',
            '趋': '之'
        }

    def getMogic(self, text):
        if text in self.resultDict:
            return self.resultDict[text]
        else:
            return False
