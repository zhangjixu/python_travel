# -*- coding: utf-8 -*-

import io
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')


def create_folder(path):
    '''
    创建文件夹
    Args:
        path:

    Returns:

    '''
    isExists = os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)


def save_file(path, content):
    '''
    保存数据到指定路径
    Args:
        path: 文件路径
        content: 保存内容

    Returns:

    '''
    with io.open(path, 'a+', encoding='utf-8') as file:
        content = str(content) + u'\n'
        file.write(content)


if __name__ == '__main__':
    for i in range(5):
        content = u'张三' + str(i)
        save_file(u'/Users/jixuzhang/Desktop/data/test.sql', content)

    print 'success'
