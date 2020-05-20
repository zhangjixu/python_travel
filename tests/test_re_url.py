# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re


def test_re():
    url = 'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode=000001&startdate=2015-01-01&enddate='
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    content = res.text.encode('unicode-escape').decode('string_escape')
    pattern = re.compile(r'^<td style="text-align: center;">(.*)<')
    result_list = re.findall(pattern, content)
    print result_list
    for result in result_list:
        print result


def test():
    content = '<td style="text-align: center;">2015-01-15</td>'
    pattern = re.compile(r'^<td style="text-align: center;">(.*)<')
    result_list = re.findall(pattern, content, re.S)
    for result in result_list:
        print result


if __name__ == '__main__':
    test()
