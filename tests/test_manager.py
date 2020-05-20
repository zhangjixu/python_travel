# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from module.OpsMysql import OpsMysql
import requests

proxies = {"http": "http://116.228.233.90:8082"}
service_args = ['--proxy=116.228.233.90:8082', '--proxy-type=http']


def test_name(page_index):
    ops_mysql = OpsMysql()
    sql = '''insert into t_fund_manager_info(`name`, `company_name`, `job_time_desc`, `fund_sum`, `profit_rate`) values(%s, %s, %s, %s, %s)'''
    url = 'http://fund.eastmoney.com/manager/#dt14;mcreturnjson;ftall;pn50;pi' + str(page_index) + ';scabbname;stasc'
    # 加载 js 生成的页面 这是无界面浏览器
    driver = webdriver.PhantomJS('/Users/jixuzhang/Documents/soft/phantomjs-2.1.1-macosx/bin/phantomjs')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', attrs={'class': 'datalist nolh'})
    th_list = table.find('thead').find('tr').find_all('th')
    # for th in th_list[1:]:
    #     # 判断 th 是否有子节点
    #     if len(th.find_all(lambda x: x.name != '', recursive=False)) > 0:
    #         print th.find('a').get_text()
    #     else:
    #         print th.get_text()

    tr_list = table.find('tbody').find_all('tr')
    save_list = []
    for tr in tr_list:
        td_list = tr.find_all('td')
        name = td_list[1].get_text()
        company_nameme = td_list[2].get_text()
        job_time_desc = td_list[4].get_text()
        fund_sum = td_list[5].get_text()
        profit_rate = td_list[6].get_text()
        save_list.append((name, company_nameme, job_time_desc, fund_sum, profit_rate))
        # print name, company_nameme, job_time_desc, fund_sum, profit_rate

    ops_mysql.inset_many(sql, save_list)


def testPage():
    url = 'http://fund.eastmoney.com/manager/#dt14;mcreturnjson;ftall;pn50;pi1;scabbname;stasc'
    # 加载 js 生成的页面
    driver = webdriver.PhantomJS('/Users/jixuzhang/Documents/soft/phantomjs-2.1.1-macosx/bin/phantomjs')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page = soup.find('span', attrs={'class': 'nv'})
    total_page = page.get_text()[1:-1]
    for page_index in range(1, int(total_page) + 1):
        test_name(page_index)


def conversion(string):
    if string.__contains__(u'年'):
        year = string[:1]
        index = string.index(u'又')
        total_days = int(year) * 365 + int(string[index + 1: -1])
    else:
        total_days = string[:-1]

    print total_days


def test():
    s = u'5年又102天'
    if s.__contains__(u'年'):
        print s[:1]
    index = s.index(u'又')
    print s[index + 1:-1]


def test_chrome():
    '''
    使用 chrome 浏览器生成 js 页面
    Returns:

    '''
    url = 'http://fund.eastmoney.com/manager/#dt14;mcreturnjson;ftall;pn50;pi1;scabbname;stasc'
    driver = webdriver.Chrome('/Users/jixuzhang/Documents/soft/chromedriver')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print soup


def crawl():
    '''
    抓取基金经理个人信息链接
    Returns:

    '''
    url = 'http://fund.eastmoney.com/manager/#dt14;mcreturnjson;ftall;pn50;pi1;scabbname;stasc'
    # 加载 js 生成的页面 这是无界面浏览器
    driver = webdriver.PhantomJS('/Users/jixuzhang/Documents/soft/phantomjs-2.1.1-macosx/bin/phantomjs')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', attrs={'class': 'datalist nolh'})
    tr_list = table.find('tbody').find_all('tr')
    for tr in tr_list:
        for tr in tr_list:
            td_list = tr.find_all('td')
            # 个人信息链接
            a_value = td_list[1].find('a')['href']
            name = td_list[1].get_text()
            test_list(name, a_value)


def test_list(name, url):
    '''
    抓取管理的基金列表
    Args:
        name: 基金经理姓名
        url: 个人信息链接

    Returns:

    '''
    ops_mysql = OpsMysql()
    sql = '''insert into t_fund_manager_info(`name`, `company_name`, `job_time_desc`, `fund_sum`, `profit_rate`) values(%s, %s, %s, %s, %s)'''
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', attrs={'class', 'ftrs'})
    tr_list = table.find('tbody').find_all('tr')
    save_list = []
    for tr in tr_list:
        td_list = tr.find_all('td')
        print name, td_list[0].get_text(), td_list[1].get_text()

    ops_mysql.inset_many(save_list)


def test():
    url = 'http://fund.eastmoney.com/manager/#dt14;mcreturnjson;ftall;pn50;pi1;scabbname;stasc'
    # 加载 js 生成的页面 这是无界面浏览器
    driver = webdriver.PhantomJS('/Users/jixuzhang/Documents/soft/phantomjs-2.1.1-macosx/bin/phantomjs',
                                 service_args=service_args)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', attrs={'class': 'datalist nolh'})
    tr_list = table.find('tbody').find_all('tr')
    for tr in tr_list:
        td_list = tr.find_all('td')
        a_value = td_list[1].find('a')['href']
        print a_value


if __name__ == '__main__':
    # conversion('102天')
    crawl()
