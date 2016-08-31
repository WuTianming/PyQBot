#!/usr/bin/env python3

import json
import sys
import collections
from xml.etree import ElementTree as etree
from urllib import request, parse

class wolfram(object):
    def __init__(self, appid):
        self.appid = appid
        self.base_url = 'http://api.wolframalpha.com/v2/query?'

    def _get_xml(self, ip):
        url_params = {'input':ip, 'appid':self.appid, 'format':'image,plaintext'}
        data = parse.urlencode(url_params).encode('utf-8')
        req = request.Request(self.base_url, data)
        xml = request.urlopen(req).read()
        return xml

    def _xmlparser(self, xml):
        data_dics = collections.OrderedDict()
        tree = etree.fromstring(xml)
        pic = ''
        # retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            for item in [ef for ef in list(e) if ef.tag=='subpod']:
                for it in [i for i in list(item) if i.tag=='plaintext' or i.tag=='img']:
                    if it.tag=='plaintext':
                        title = e.get('title')
                        if title == None:
                            continue
                        elif title == 'Plot':
                            title = '绘图'
                        elif title == 'Input':
                            title = '输入'
                        elif title == 'Result' or title == 'Value':
                            title = '结果'
                        elif title == 'Response':
                            title = '回复'
                        elif title == 'Solution' or title == 'Solutions':
                            title = '方程的解'
                        elif title == 'Exact result':
                            title = '准确值'
                        elif title == 'Decimal approximation':
                            title = '近似值'
                        elif title == 'Input interpretation':
                            title = '问题分析'
                        elif title == 'Details':
                            title = '详细信息'
                        elif title == 'Scientific notation':
                            title = '科学计数法'
                        elif title == 'Number name' or title == 'Number names':
                            title = '数名'
                        elif title == 'Roman numerals':
                            title = '罗马数字'
                        elif title == 'Binary form':
                            title = '二进制'
                        elif title == 'Prime factorization':
                            title = '因数分解'
                        elif title == 'Property' or title == 'Properties':
                            title = '其他信息'
                        elif title == 'Alternate form' or title == 'Alternate forms':
                            title = '其他形式'
                        elif title == 'Number length':
                            title = '数字长度'
                        elif title == 'Root' or title == 'Roots':
                            title = '根'
                        elif title == 'Series expansion at x=0':
                            title = 'x为0时的展开'
                        elif title == 'Limit':
                            title = '极限'
                        elif title == 'Visual representation':
                            title = '可视化表示'
                        elif title == 'Number line':
                            title = '数轴'
                        elif 'comparsion' in title.lower():
                            continue
                        elif 'reference' in title.lower():
                            continue
                        elif title == 'Ranking':
                            continue
                        elif title == 'Derivative':
                            continue
                        elif title == 'Periodicity':
                            continue
                        elif title == 'Manipulatives illustration':
                            continue
                        elif title == 'Percent increase':
                            continue
                        elif title == 'Residues modulo small integers':
                            continue
                        elif title == 'Typical human computation times':
                            continue
                        else:
                            pass
                        if it.text == None:
                            data_dics[title] = pic
                        else:
                            data_dics[title] = it.text
                    elif it.tag=='img':
                        title = e.get('title')
                        if it.attrib['title'] == '':
                            # print(it.attrib['src'])
                            pic = it.attrib['src']
        return data_dics
    def search(self, ip):
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        return result_dics

if __name__ == "__main__":
    a = wolfram('P4TW4v-XYLLG3XXEU')
    print(a.search('y=x^2'))
