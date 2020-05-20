# -*- coding: utf-8 -*-

import itertools
import sys
import time
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from grab import crawl_bank_post

reload(sys)
sys.setdefaultencoding('utf-8')


def test_draw(x, y, y1):
    '''
    画图
    Args:
        x: x 轴坐标数值
        y: y 轴坐标数值
        y1: y1 轴坐标数值

    Returns:

    '''
    # 使 y 轴按照升序排序
    lists = sorted(itertools.izip(*[x, y]))
    lists1 = sorted(itertools.izip(*[x, y1]))
    new_x, new_y = list(itertools.izip(*lists))
    new_x, new_y1 = list(itertools.izip(*lists1))
    # 把字符串日期变为 datetime 类型
    xs = [datetime.strptime(d, '%Y.%m.%d %H:%M:%S') for d in new_x]
    # 配置横坐标
    ax = plt.gca()
    # 定义 x 轴时间格式
    dfm = mdates.DateFormatter('%Y.%m.%d %H:%M:%S')
    # x 轴时间格式设置
    ax.xaxis.set_major_formatter(dfm)
    # o-:圆形
    plt.plot(xs, new_y, 'o-', color='r', label='$')
    # r-:方形
    plt.plot(xs, new_y1, 'r-', color='b', label='£')
    # 横坐标名字
    plt.xlabel('cdate')
    # 纵坐标名字
    plt.ylabel('price')
    # 图例
    plt.legend(loc='best')
    # plot
    # 自动旋转日期标记
    plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == '__main__':
    start_time = time.time()
    x = []
    y = []
    y1 = []
    list_data = crawl_bank_post.crawl_bank('2015-01-01', '2015-01-01', '美元', False)
    list_data1 = crawl_bank_post.crawl_bank('2015-01-01', '2015-01-01', '英镑', False)
    for data in list_data:
        x.append(data[6])
        y.append(data[5])

    for data1 in list_data1:
        y1.append(data[5])

    test_draw(x, y, y1)
    cost_time = time.time() - start_time
    print 'cost time : %.2f s' % cost_time
