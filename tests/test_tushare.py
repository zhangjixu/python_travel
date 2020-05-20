# -*- coding: utf-8 -*-

import tushare as ts


def test_movie():
    df = ts.realtime_boxoffice()
    print df


if __name__ == '__main__':
    test_movie()
