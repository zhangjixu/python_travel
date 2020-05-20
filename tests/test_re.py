# -*- coding: utf-8 -*-

import re
import io


def test_re():
    pattern_1 = '(var m_nRecordCount = )'
    p = re.compile(pattern_1)
    str_1 = p.sub('', '''www 
        var m_nRecordCount = 56695;
        var m_nPageSize = 20;
        aa''')
    str = p.sub('', str_1)

    pattern_2 = '(;)'
    p = re.compile(pattern_2)
    str = p.sub('', str)
    print str


def test_re_1():
    pattern = '\n'
    p = re.compile(pattern)
    str_1 = p.sub('', '''www 
    var m_nRecordCount = 56695;
    var m_nPageSize = 20;
    aa''')
    str = p.sub('', str_1)
    print str


def test_split():
    with io.open("/Users/jixuzhang/Desktop/data/test/ip.txt", "r") as file:
        a = set()
        b = {}
        for data in file.readlines():
            arr = data.split(" ")
            a.add(arr[0])
            b[arr[0]] = 0

        for index in a:
            if b[index] != 0:
                print index


def test_tup():
    return (1, "name")


def test_set():
    strs = "22"
    if "22" in strs:
        print 1


def test_():
    for _ in range(20):
        print _


if __name__ == '__main__':
    test_()
