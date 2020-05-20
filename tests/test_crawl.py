# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_page_no():
    url = 'http://srh.bankofchina.com/search/whpj/search.jsp'


def parse_html_post(content):
    # print content
    # 创建 beautifulsoup 对象并使用 html 解析器
    soup = BeautifulSoup(content, 'html.parser')
    script_list = soup.find_all('script', attrs={'language': 'JavaScript'})
    # print script_list[3].get_text()
    # for script in script_list:
    #     print '============'
    #     print script.get_text()

    str_list = script_list[3]
    string = str_list.get_text().split('\n')
    str_1 = string[12]
    str_2 = string[17]
    max_count_record = str_1[22:-2]
    page_size = str_2[19:-2]
    page_no = int(max_count_record) / int(page_size) if int(max_count_record) % int(page_size) == 0 else int(
        max_count_record) / int(page_size) + 1
    print page_no
    # for index, st in enumerate(string):
    #     print index, st
    # pattern = '\n'
    # p = re.compile(pattern)
    # str = p.sub('', str_list.get_text().encode('UTF-8'))
    # print '================ %s ' %  str_list.get_text().encode('UTF-8'), '================ %s ' %  type(str_list.get_text().encode('UTF-8'))
    # pattern = '((var m_nRecordCount = [\d]+))'
    # p = re.compile(pattern)
    # str = p.sub('===============================', str)
    # print str
    # for script in script_list:
    #     print script.get_text()
    # 获取所有 tr 的标签，排除第一个
    # list_tr = soup.find_all('tr')[1:]
    # for tr in list_tr:
    #     pass
    #     print tr.get_text()


def parse_html_get(content):
    # print content
    # 创建 beautifulsoup 对象并使用 html 解析器
    soup = BeautifulSoup(content, 'html.parser')
    # 获取所有 tr 的标签，排除第一个
    turn_page = soup.find('div', attrs={'class': 'turn_page'})
    print turn_page.p.span.get_text()


def crawl_bank_get():
    url = 'http://www.boc.cn/sourcedb/whpj/index.html'
    # 发送 http get 请求
    res = requests.get(url)
    res.encoding = 'utf-8'
    content = res.text
    parse_html_get(content)


def crawl_bank_post():
    url = 'http://srh.bankofchina.com/search/whpj/search.jsp'
    payload = {'erectDate': '2018-11-11', 'nothing': '', 'pjname': 1315}
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.post(url, payload, headers=headers)
    res.encoding = 'utf-8'
    # 获取 http 请求响应数据
    content = res.text
    parse_html_post(content)


if __name__ == '__main__':
    crawl_bank_post()
