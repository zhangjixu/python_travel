# -*- coding: utf-8 -*-

from module.OpsMysql import OpsMysql


def test_mysql():
    ops_mysql = OpsMysql()
    sql = """insert into SC(SID) values(%s)"""
    ops_mysql.inset_many(sql, [(1,)])


def test_query():
    ops_mysql = OpsMysql()
    sql = """ select * from Student; """
    datas = ops_mysql.query(sql)
    for data in datas:
        print data


if __name__ == '__main__':
    test_mysql()
    print "success"
