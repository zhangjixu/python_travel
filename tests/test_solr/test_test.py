# -*- coding: utf-8 -*-

if __name__ == '__main__':
    array = ["File	Position	Binlog_Do_DB	Binlog_Ignore_DB	Executed_Gtid_Set",
             "mysql-bin.000001	1021	"]
    for i in array[1].split("\t"):
        print i