# -*- coding: utf-8 -*-


def success(msg):
    print msg


def debug(msg):
    print msg


def error(msg):
    print msg


def warning(msg):
    print msg


def other(msg):
    print msg


def notify_result(num, msg):
    numbers = {
        0: success,
        1: debug,
        2: warning,
        3: error
    }

    method = numbers.get(num, other)
    if method:
        method(msg)


if __name__ == '__main__':
    # 检测字符串是否由字母和数字组成。
    str_ = '123kjh'
    print str_.isalnum()
    notify_result(2, 'debug')
