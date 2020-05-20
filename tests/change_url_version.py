# -*- coding: utf-8 -*-

import time
import json
import math
import numpy as np
import requests
from utils import logger

DATETIME_FORMAT = '%Y-%m-%d'
log = logger.log


def str_json():
    string = u'1314:英镑,1315:港币,1316:美元,1317:瑞士法郎,1318:德国马克,1319:法国法郎,1375:新加坡元,1320:瑞典克朗,1321:丹麦克朗,' \
             u'1322:挪威克朗,1323:日元,1324:加拿大元,1325:澳大利亚元,1326:欧元,1327:澳门元,1328:菲律宾比索,1329:泰国铢,1330:新西兰元,' \
             u'1331:韩元,1843:卢布,2890:林吉特,2895:新台币,1370:西班牙比塞塔,1371:意大利里拉,1372:荷兰盾,1373:比利时法郎,1374:芬兰马克,' \
             u'3030:印尼卢比,3253:巴西里亚尔,3899:阿联酋迪拉姆,3900:印度卢比,3901:南非兰特,4418:沙特里亚尔,4560:土耳其里拉'
    list_str = string.split(',')
    dic = {}
    for str in list_str:
        arr = str.split(':')
        dic[arr[1]] = arr[0]

    for key, value in dic.iteritems():
        print key
        print value


def test_date(start_date):
    try:
        if not start_date:
            print ' ========== ' + start_date
            time.strptime(start_date, DATETIME_FORMAT)

        print start_date
    except Exception as e:
        raise Exception(e)


def str_json():
    '''
    字符串转 json 格式数据
    :return:
    '''
    json_str = u'''{"name":"张三", "json":{"name":"李四"}}'''
    json_obj = json.loads(json_str)
    print type(json_obj)
    print json_obj['json']['name']


def test_raw():
    str_ = raw_input("请输入：")
    print '您输入的是 ', str_


def cost_time(fun):
    '''
    自定义装饰器，用于统计函数执行时间
    Args:
        fun: 执行函数

    Returns:

    '''

    def wrapper(*args, **kwargs):
        start = time.time()
        fun(*args, **kwargs)
        print '============ ', args, kwargs
        cost = int(time.time() - start)
        print 'cost time:', cost, 's'

    return wrapper


@cost_time
def count_api(name, age):
    age = 19
    # print 'name: ', name, 'age: ', age


def adder(x):
    '''
    闭包概念
    Args:
        x:

    Returns:

    '''

    def wrapper(y):
        return x + y

    return wrapper


def get(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print r.content
        else:
            print r.status_code
    except Exception as e:
        print e


def getVersion():
    get(u'http://10.76.85.201:8080/hbase_service/sn/queryVersion')
    get(u'http://10.76.85.202:8080/hbase_service/sn/queryVersion')
    get(u'http://10.76.85.203:8080/hbase_service/sn/queryVersion')
    get(u'http://10.76.85.204:8080/hbase_service/sn/queryVersion')
    get(u'http://10.76.85.205:8080/hbase_service/sn/queryVersion')


if __name__ == '__main__':
    # 20190301 1551369600000
    # count_api('name', age=18)
    # get(u'http://10.76.85.201:8080/hbase_service/sn/modifySnVersion/1551369600000')
    # get(u'http://10.76.85.202:8080/hbase_service/sn/modifySnVersion/1551369600000')
    # get(u'http://10.76.85.203:8080/hbase_service/sn/modifySnVersion/1551369600000')
    # get(u'http://10.76.85.204:8080/hbase_service/sn/modifySnVersion/1551369600000')
    # get(u'http://10.76.85.205:8080/hbase_service/sn/modifySnVersion/1551369600000')
    getVersion()
