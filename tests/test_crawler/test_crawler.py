# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json


def get_url():
    '''
    从该页面爬取 所有基金代码、基金名称、基金ＵＲＬ
    Returns:

    '''
    base_url = 'http://fund.eastmoney.com/allfund.html'
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.get(base_url, headers=headers)
    res.encoding = 'gb2312'
    # 获取 http 请求响应数据
    content = res.text
    # print content
    # 创建 beautifulsoup 对象并使用 html 解析器
    soup = BeautifulSoup(content, 'html.parser')
    # 这个页面的基金代码分别放在 'class="num_box" 对应的 div 中
    fund_url_list = soup.find_all('div', attrs={'class': 'num_box'})
    for url in fund_url_list:
        ## 具体的基金名称，url 等信息放在 li 中
        li_list = url.find('ul').find_all('li')
        for li in li_list:
            try:
                a_atts_list = li.find('div').find_all('a')
                fund_name = a_atts_list[0].get_text()
                fund_url = a_atts_list[0]['href']
                tieba_name = a_atts_list[1].get_text()
                tieba_url = a_atts_list[1]['href']
                archives_name = a_atts_list[2].get_text()
                archives_url = a_atts_list[2]['href']
                print fund_url, fund_name, tieba_url, tieba_name, archives_url, archives_name
            except:
                continue


def get_detail(base_url):
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.get(base_url, headers=headers)
    res.encoding = 'utf-8'
    # 获取 http 请求响应数据
    content = res.text
    print content
    # 创建 beautifulsoup 对象并使用 html 解析器
    soup = BeautifulSoup(content, 'html.parser')
    ## 获取净值估算信息
    # by_id = soup.find('dl', attrs={'class': 'dataItem01'})
    # span_list = by_id.find('dt').find('p').find_all('span')
    # ## 净值估算
    # net_worth = span_list[0].get_text()
    # ## 时间
    # date = span_list[2].get_text()
    # print net_worth, date

def test(base_url):
    driver = webdriver.PhantomJS('D:\\soft\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup)

if __name__ == '__main__':
    # get_url()
    # get_detail('http://fund.eastmoney.com/000001.html')
     test('http://fund.eastmoney.com/000001.html')
    # list = []
    # list.append({"在": "是"})
    # print json.dumps(list[0], ensure_ascii=False, encoding='UTF-8')
