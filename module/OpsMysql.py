# -*- coding: utf-8 -*-

from module.MySQLUtils import MySQLUtils
from conf import mysql_conf as cfg


class OpsMysql(object):
    '''
    用于操作 mysql 数据库
    '''

    def query(self, sql, value=None):
        '''
        用于执行查询语句
        Args:
            sql: 执行的 sql 语句
            value: 语句中的参数列表

        Returns:

        '''
        with MySQLUtils(host=cfg.MYSQL_ALPHACASH_HOST, port=cfg.MYSQL_ALPHACASH_PORT,
                        user=cfg.MYSQL_ALPHACASH_ADMIN_USER, password=cfg.MYSQL_ALPHACASH_ADMIN_PWD,
                        database=cfg.MYSQL_ALPHACASH_DB) as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(sql, value)
            return cur.fetchall()

    def update(self, sql, value=None):
        '''
        执行 增 删 改 语句
        Args:
            sql: 执行的 sql 语句
            value: 语句中的参数列表

        Returns:

        '''
        with MySQLUtils(host=cfg.MYSQL_ALPHACASH_HOST, port=cfg.MYSQL_ALPHACASH_PORT,
                        user=cfg.MYSQL_ALPHACASH_ADMIN_USER, password=cfg.MYSQL_ALPHACASH_ADMIN_PWD,
                        database=cfg.MYSQL_ALPHACASH_DB) as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(sql, value)
            cnx.commit()

    def inset_many(self, sql, value=None):
        '''
        用于批量保存数据
        Args:
            sql: 执行的 sql 语句
            value: 语句中的参数列表

        Returns:

        '''
        with MySQLUtils(host=cfg.MYSQL_ALPHACASH_HOST, port=cfg.MYSQL_ALPHACASH_PORT,
                        user=cfg.MYSQL_ALPHACASH_ADMIN_USER, password=cfg.MYSQL_ALPHACASH_ADMIN_PWD,
                        database=cfg.MYSQL_ALPHACASH_DB) as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.executemany(sql, value)
            cnx.commit()
