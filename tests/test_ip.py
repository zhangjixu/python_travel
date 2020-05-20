# -*- coding: utf-8 -*-

import time

import requests
from bs4 import BeautifulSoup

from module.OpsMysql import OpsMysql


def response():
    pass


def test3(code, proxies):
    DATETIME_FORMAT = '%Y-%m-%d'
    st = time.localtime()
    today = time.strftime(DATETIME_FORMAT, st)

    # 代理 ip


    url = 'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode=' + str(
        code) + '&startdate=2015-01-01&enddate=' + today
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.get(url, headers=headers, proxies=proxies)
    res.encoding = 'gbk'
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    # 获取名称
    name_list = soup.find('table', attrs={'class': 'n_table m_table'}).find('thead').find('tr').find_all('th')
    # 发布日期
    release_date = name_list[0].get_text()
    # 单位净值
    value_unit = name_list[1].get_text()
    # 累计净值
    cumulative_value = name_list[2].get_text()
    # 日增长率
    day_growth = name_list[3].get_text()
    # print release_date, value_unit, cumulative_value, day_growth
    # 具体数字的列表
    tr_list = soup.find('table', attrs={'class': 'n_table m_table'}).find('tbody').find_all('tr')
    print len(tr_list)
    for tr in tr_list:
        try:
            # 各个名称对应的值
            td_list = tr.find_all('td')
            print code, td_list[0].get_text(), td_list[1].get_text(), td_list[2].get_text(), td_list[3].get_text()
        except Exception as e:
            print e.message
            continue


def test4(proxies):
    ops_mysql = OpsMysql()
    sql = '''select a.fund_code from t_fund_info a left join t_fund_trade b on a.fund_code = b.fund_code  where  a.id is null or b.id is null;'''
    data_list = ops_mysql.query(sql)
    for data in data_list:
        test3(data['fund_code'], proxies)
        # break
        # print type(data['fund_code']), data['fund_code']


def test5():
    pass


if __name__ == '__main__':
    proxies = {"http": "http://116.228.233.90:8082"}
    test4(proxies)
    # test3(000002, proxies)
