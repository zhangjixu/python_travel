# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import pymongo
from conf import mongo_conf

# 日期格式化
DATETIME_FORMAT = '%Y-%m-%d'
client = pymongo.MongoClient(host=mongo_conf.ip, port=mongo_conf.port)
# 指定 db
db = client['test']
# 定义全局变量 tuple_list
tuple_list = []

# 初始化数据
string = '1314:英镑,1315:港币,1316:美元,1317:瑞士法郎,1318:德国马克,1319:法国法郎,1375:新加坡元,1320:瑞典克朗,1321:丹麦克朗,1322:挪威克朗,' \
         '1323:日元,1324:加拿大元,1325:澳大利亚元,1326:欧元,1327:澳门元,1328:菲律宾比索,1329:泰国铢,1330:新西兰元,1331:韩元,1843:卢布,2890:林吉特,' \
         '2895:新台币,1370:西班牙比塞塔,1371:意大利里拉,1372:荷兰盾,1373:比利时法郎,1374:芬兰马克,3030:印尼卢比,3253:巴西里亚尔,3899:阿联酋迪拉姆,' \
         '3900:印度卢比,3901:南非兰特,4418:沙特里亚尔,4560:土耳其里拉'
list_str = string.split(',')
dic = {}

for str in list_str:
    arr = str.split(':')
    dic[arr[1]] = arr[0]


def get_page_no(start_date, end_date, pjname):
    '''
    获取页面的最大页数
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param pjname: 牌价名称
    :return:
    '''

    url = 'http://srh.bankofchina.com/search/whpj/search.jsp'
    # post 的请求数据
    payload = {'erectDate': start_date, 'nothing': end_date, 'pjname': dic[pjname]}
    # 构建 headers 信息
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送 http post 请求
    res = requests.post(url, payload, headers=headers)
    res.encoding = 'utf-8'
    # 获取 http 请求响应数据
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    script_list = soup.find_all('script', attrs={'language': 'JavaScript'})

    str_list = script_list[3]
    string = str_list.get_text().split('\n')
    str_1 = string[12]
    str_2 = string[17]
    max_count_record = str_1[22:-2]
    page_size = str_2[19:-2]
    page_no = int(max_count_record) / int(page_size) if int(max_count_record) % int(page_size) == 0 else int(
        max_count_record) / int(page_size) + 1

    return page_no


def parse_html(content):
    '''
    解析网页
    :param content: requests 请求后返回的 response 内容
    :param page_index: 第 page_index 页
    :return:
    '''

    global tuple_list
    try:
        # 创建 beautifulsoup 对象并使用 html 解析器
        soup = BeautifulSoup(content, 'html.parser')
        # 获取所有 tr 的标签，排除第一个
        list_tr = soup.find_all('tr')[2:-1]
        for tr in list_tr:
            str = tr.get_text().split('\n')[1:]
            # 把序列转换为元祖
            tup = tuple(str)
            print tup
            # 把元祖保存到序列中
            tuple_list.append(tup)

        # tuple_list.append(tuple_list(list_tr))
    except Exception as e:
        print 'parse_html exception: %s' % (e)
        raise Exception(e)


def crawl_bank(start_date, end_date, pjname, flag=True):
    '''
    解析中国银行牌价信息
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param pjname: 牌价名称
    :param flag: 是否保存数据到 mongo
    :return:
    '''
    try:
        if start_date is not '':
            time.strptime(start_date, DATETIME_FORMAT)

        if end_date is not '':
            time.strptime(end_date, DATETIME_FORMAT)

    except Exception as e:
        print '时间格式不正确 %s' % (e)
        return

    if pjname in dic:
        # post 请求的 url
        url = 'http://srh.bankofchina.com/search/whpj/search.jsp'
        # 获取最大页面数
        page_no = get_page_no(start_date, end_date, pjname)
        if page_no > 0:
            for i in range(1, page_no + 1):
                # post 的请求数据
                payload = {'erectDate': start_date, 'nothing': end_date, 'pjname': dic[pjname], 'page': i}
                # 构建 headers 信息
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                # 发送 http post 请求
                res = requests.post(url, payload, headers=headers)
                res.encoding = 'utf-8'
                # 获取 http 请求响应数据
                content = res.text
                parse_html(content)
            if flag:
                save_mongo(start_date, end_date, pjname)
            else:
                return tuple_list
    else:
        print '无此牌价'


def save_mongo(start_date, end_date, pjname):
    '''
    把数据保存到 mongodb 中
    :param start_date: 搜索开始时间
    :param end_date: 搜索结束时间
    :param pjname: 牌价名称
    :return:
    '''
    global tuple_list
    # 搜索内容为空退出
    if len(tuple_list[0]) == 2:
        print 'tuple_list 为空'
        return
    # 创建空的 json 序列
    list_json = []
    # 指定 collection
    collection = db.bank_quotation
    k = 0
    documents = []
    for tup in tuple_list:
        document = {'start_date': start_date, 'end_date': end_date, 'pjname': pjname, 'currency_name': tup[0],
                    'buy_rate_change': tup[1], 'buy_rate_cash': tup[2], 'spot_rate': tup[3],
                    'cash_seling_rate': tup[4], 'boc_price': tup[5], 'release_date': tup[6]}
        documents.append(document)
        k += 1
        if k % 10000 is 0:
            collection.insert
            # 批量 (10000条) 保存数据到 bank_quotation
            collection.insert_many(documents)
            # 清空序列
            documents = []

    if k % 10000 is not 0:
        collection.insert_many(documents)
        # 清空序列
        documents = []

    print ' k : %s tuple_list : %s' % (k, len(tuple_list))
    # 每次保存完数据后，清空 tuple_list
    tuple_list = []


if __name__ == '__main__':
    start_time = time.time()
    crawl_bank('2007-11-08', '2018-11-08', '土耳其里拉')
    cost_time = time.time() - start_time
    print 'success cost time : %.2f s' % (cost_time)
