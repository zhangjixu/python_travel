# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re
import execjs
import time
from module.OpsMysql import OpsMysql


def test():
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # 获取 http 请求响应数据
    content = res.text
    list = content[9:]

    for i in list:
        print i
    # soup = BeautifulSoup(content, 'html.parser')
    # p = re.compile('/var r = (.*);/')
    # print p


def test1():
    ops_mysql = OpsMysql()
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    content = res.text
    # 截取表达式
    string = content[9:-1]
    # 转换为 list
    list_str = eval(string)
    # print list_str[0]
    sql = '''insert into `t_fund_info`(`fund_code`, `fund_name`, `fund_name_cn`, `fund_type`) values(%s, %s, %s, %s)'''
    save_list = []
    for list in list_str:
        save_list.append((list[0], list[1], list[2], list[3]))

    ops_mysql.inset_many(sql, save_list)
    print " success ===================== "


def test2():
    ops_mysql = OpsMysql()
    sql = '''select fund_code from t_fund_info;'''
    data = ops_mysql.query(sql)
    for i in data:
        print i


def test3(code):
    ops_mysql = OpsMysql()
    sql = '''insert into t_fund_trade(fund_code, fld_enddate, fld_unitnetvalue, fld_accunetvalue, fld_dailygrowthrate, cdate) values(%s, %s, %s, %s, %s, now()) '''
    DATETIME_FORMAT = '%Y-%m-%d'
    st = time.localtime()
    today = time.strftime(DATETIME_FORMAT, st)
    url = 'http://jingzhi.funds.hexun.com/DataBase/jzzs.aspx?fundcode=' + str(
        code) + '&startdate=2015-01-01&enddate=' + today
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 代理 ip
    # proxies = {"http": "http://106.14.5.129:80"}
    # 发送 http post 请求
    res = requests.get(url, headers=headers)
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
    save_list = []
    for tr in tr_list:
        try:
            # 各个名称对应的值
            td_list = tr.find_all('td')
            # print code, td_list[0].get_text(), td_list[1].get_text(), td_list[2].get_text(), td_list[3].get_text()
            save_list.append(
                (code, td_list[0].get_text(), td_list[1].get_text(), td_list[2].get_text(), td_list[3].get_text()))
            # print code, td_list[0].get_text(), td_list[1].get_text(), td_list[2].get_text(), td_list[3].get_text()
        except Exception as e:
            print e.message
            continue
    try:
        ops_mysql.inset_many(sql, save_list)
    except Exception as e:
        print e.message


def test4():
    # 暂停 5 秒
    time.sleep(5)
    ops_mysql = OpsMysql()
    sql = '''select a.fund_code from t_fund_info a left join t_fund_trade b on a.fund_code = b.fund_code  where  a.id is null or b.id is null;'''
    data_list = ops_mysql.query(sql)
    print len(data_list)
    for data in data_list:
        test3(data['fund_code'])
        # break
        # print type(data['fund_code']), data['fund_code']


def test5():
    # 000001 2019-04-19 1.1730 3.5840 0.43%
    ops_mysql = OpsMysql()
    sql = '''select a.fund_code from t_fund_info a left join t_fund_trade b on a.fund_code = b.fund_code  where  a.id is null or b.id is null; '''
    data = ops_mysql.query(sql)
    print len(data)

def test6():
    list_str = [1, 2, 3, 4, 5]

class Test:
    def test(self):
        return 2

    def test1(self):
        s = self.test()
        print s

if __name__ == '__main__':
    test = Test()
    test.test1()
