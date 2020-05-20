# -*- coding: utf-8 -*-

import os


def test_os():
    # 获取操作系统类型，nt: windows posix: linux
    print '操作系统类型为: %s' % os.name
    print '操作系统换行符为: %s' % os.linesep
    print '操作系统分隔符为: %s' % os.sep
    print '返回当前的工作目录: %s' % os.getcwd()
    # 边路目录树，包括子目录
    list_file = os.walk('/Users/jixuzhang/Desktop/data/test')
    for file in list_file:
        print file

    print '返回指定工作目录下的文件和目录信息: %s' % os.listdir(u'/Users/jixuzhang/Desktop/data')
    # 创建多级目录: /Users/jixuzhang/Desktop/data/ddd
    os.makedirs(u'/Users/jixuzhang/Desktop/data/ddd/ddd/dddd')
    # 删除目录
    os.removedirs(u'/Users/jixuzhang/Desktop/data/ddd/ddd/dddd')
    # 删除文件
    # os.remove(u'/Users/jixuzhang/Desktop/data/test/io/xjbk.txt')
    print '判断文件或路径是否存在: %s ' % os.path.exists('/Users/jixuzhang/Desktop/data/test/io/test.txt')
    print '获取文件的绝对路径: %s' % os.path.abspath('test_file.py')
    print '拼接路径: %s:' % os.path.join('/User/zw/program/Python/Code', 'demoe/message.txt')
    # 重命名文件名
    # os.rename(u'/Users/jixuzhang/Desktop/data/test/io/name.txt', u'/Users/jixuzhang/Desktop/data/test/io/rename.txt')
    print '获取文件的基本信息: %s' % os.stat('/Users/jixuzhang/Desktop/data/test/io/rename.txt')


if __name__ == '__main__':
    test_os()
