# -*- coding: utf-8 -*-

import io


def test_file():
    '''
    操作文件
    r 只读，文件不存在报错
    r+ 打开文件后，可读可写（写会覆盖原来的内容）文件不存在报错
    w 只写模式打开，文件存在清空
    w+ 可读可写，打开文件后清空原有文件
    a+ 以读写模式打开文件，文件存在则在文件末尾进行追加，否则创建新文件
    a 以追加模式打开一个新文件，只能用于写

    对于'r+'来说，如果先读取了内容，再写入的话就变成了追加的模式，如果直接写入内容，就是覆盖了
    :return:
    '''
    # buffering = 1 写入一行缓存到硬盘
    # buffering = 0 默认策略，写入任意大小数据都缓存到硬盘
    # buffering > 1 写入指定大小数据，缓存到硬盘
    file = io.open('/Users/jixuzhang/Desktop/data/test/io/test.txt', 'a+', encoding='utf-8', buffering=1)
    file.seek(0)
    # 这是读取全部行，返回的是一个字符串列表，所以文件很大时不建议使用
    for data in file.readlines():
        print data.strip('\n')

    file.close()


def test_with():
    '''
    当我们写文件时，操作系统往往不会立刻把数据写入磁盘，而是放到内存缓存起来，空闲的时候再慢慢写入。
    只有调用close()方法时，操作系统才保证把没有写入的数据全部写入磁盘。忘记调用close()的后果是数据可能只写了一部分到磁盘，
    剩下的丢失了。所以，还是用with语句来得保险
    :return:
    '''
    with io.open('/Users/jixuzhang/Desktop/data/test/io/test.txt', 'a+', encoding='utf-8') as file:
        file.seek(0)
        number = 0
        while True:
            number += 1
            line = file.readline()
            print number, line
            if line == '':
                break


if __name__ == '__main__':
    test_file()
