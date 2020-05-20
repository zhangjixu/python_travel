# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def test_plot():
    '''
    一张图标显示一个图形
    Returns:

    '''
    # 在 -3 到 3 之间均匀取 50 个点
    x = np.linspace(-3, 3, 50)
    y1 = 2 * x + 1
    y2 = x ** 2
    # 创建绘图对象 1
    plt.figure(num=1, figsize=(8, 5), )
    plt.plot(x, y1, color='red', linewidth=2)
    # x 轴标签
    plt.xlabel('x shaft')
    # y 轴标签
    plt.ylabel('y shaft')
    # 标题
    plt.title('histogram')
    # 创建绘图对象 2 序号大显示在最前面
    plt.figure(num=2, figsize=(8, 5), )
    plt.plot(x, y2, label='c', color='black', linewidth=2)
    plt.xlabel('xx')
    plt.ylabel('yy')
    plt.title('curve')
    # 显示图例
    plt.legend()
    plt.show()


def test_plot_1():
    '''
    一张图表显示两个图形
    Returns:

    '''
    x = np.linspace(-3, 3, 50)
    y1 = 2 * x + 1
    y2 = x ** 2
    plt.plot(x, y1, label='1', color='r')
    plt.plot(x, y2, label='2', color='b')
    # 显示图例
    plt.legend()
    plt.show()


def test_plot_2():
    '''
    x 轴显示日期
    Returns:

    '''
    x = ['2018-10-01 15:00:00', '2018-10-01 16:00:00', '2018-10-01 17:00:00', '2018-10-01 18:00:00',
         '2018-10-01 19:00:00']
    y = [10, 3, 13, 9, 10]
    xs = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in x]
    # 配置 x 轴为时间格式
    ax = plt.gca()
    # 定义 x 轴时间格式
    dfm = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    # 设置 x 轴时间格式
    ax.xaxis.set_major_formatter(dfm)
    plt.plot(xs, y)
    # 自动旋转日期标记
    plt.gcf().autofmt_xdate()
    plt.show()


def test_plot_3():
    '''
    不用格式化日期
    显示日期
    Returns:

    '''
    x = ['2018-10-01 15:00:00', '2018-10-01 16:00:00', '2018-10-01 17:00:00', '2018-10-01 18:00:00',
         '2018-10-01 19:00:00']
    y = [10, 3, 13, 9, 10]
    plt.plot(x, y)
    # 自动旋转日期标记
    plt.gcf().autofmt_xdate()
    plt.show()


def test_plot_4():
    '''
    显示多个图
    Returns:

    '''
    x = ['2018-10-01 15:00:00', '2018-10-01 16:00:00', '2018-10-01 17:00:00', '2018-10-01 18:00:00',
         '2018-10-01 19:00:00']
    y1 = [10, 3, 13, 9, 10]
    y2 = [8, 6, 12, 7, 9]
    y3 = [8, 6, 12, 7, 9]
    y4 = [8, 6, 12, 7, 9]
    # 两行两列的第 1 个图
    plt.subplot(2, 2, 1)
    plt.plot(x, y1)
    plt.gcf().autofmt_xdate()
    # 两行两列的第 2 个图
    plt.subplot(2, 2, 2)
    plt.gcf().autofmt_xdate()
    plt.plot(x, y2)
    # 两行两列的第 3 个图
    plt.subplot(2, 2, 3)
    plt.gcf().autofmt_xdate()
    plt.plot(x, y3)
    # 两行两列的第 4 个图
    plt.subplot(2, 2, 4)
    plt.gcf().autofmt_xdate()
    plt.plot(x, y4)
    plt.show()


if __name__ == '__main__':
    # test_plot()
    print(2)
