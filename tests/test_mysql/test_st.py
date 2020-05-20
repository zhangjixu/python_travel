# -*- coding: utf-8 -*-

import io
import os
import sys
import paramiko
from module.OpsMysql import OpsMysql

reload(sys)
sys.setdefaultencoding('utf-8')


def test_split():
    with io.open("/Users/jixuzhang/Desktop/data/test/2.txt", "r") as file:
        cabinet = "1-4B-L02"
        arr = []
        for data in file.readlines():
            arrs = data.split("\t")
            physical_sn = arrs[0]
            physical_ip = arrs[1].replace("\n", "")
            # arr.append((cabinet, physical_sn, physical_ip))
            get_avaliable_connection(cabinet, physical_sn, physical_ip)

        return arr


def get_avaliable_connection(cabinet, physical_sn, physical_ip):
    '''
    获取可用的连接
    Args:
        host:

    Returns:

    '''
    available = {"psadmin": "PS123abc,.", "root": "123abc,.", "root_second": "ps123abc,."}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for user, password in available.items():
        try:
            ssh.connect(physical_ip, 22, user.replace("root_second", "root"), password)
            break
        except Exception:
            continue

    get_physical_machine_info(cabinet, physical_sn, physical_ip, ssh, password)


def get_physical_machine_info(cabinet, physical_sn, physical_ip, ssh, password):
    '''
    获取物理机信息
    Args:
        host:

    Returns:

    '''
    try:

        # 获取物理机虚拟机信息
        vm_stdin, vm_stdout, vm_stderr = ssh.exec_command('sudo virsh list --all --title', get_pty=True)
        vm_stdin.write(password + "\n")
        result_vm = vm_stdout.read().decode('utf-8')
        # 统计虚拟机 ip 数量
        count_ip = 0

        stdin, stdout, stderr = ssh.exec_command('sudo virsh list --all --title', get_pty=True)

        sqls = []
        flag = True
        if "command not found" not in result_vm:
            for vm in stdout:
                count_ip += 1
                get_ip(vm)
                # get_ip_result = get_ip(vm)
                # if len(get_ip_result) > 0:
                #     vm_ip = get_ip_result[0]
                #     vm_status = get_ip_result[1]
                #     sqls.append((cabinet, physical_sn, physical_ip, vm_ip, vm_status))
        # else:
        #     flag = False
        #     sqls = [(cabinet, physical_sn, physical_ip), ]
        #
        # test_save_mysql(sqls, flag)

    except Exception as e:
        print e.message
    finally:
        ssh.close()


def test_save_mysql(sqls, flag):
    ops_mysql = OpsMysql()
    if flag:
        sql = """ insert into `server_info`(`cabinet`, `physical_sn`, `physical_ip`, `vm_ip`, `vm_status`) values(%s, %s, %s, %s, %s) """
    else:
        sql = """ insert into `server_info`(`cabinet`, `physical_sn`, `physical_ip`) values(%s, %s, %s) """
    ops_mysql.inset_many(sql, sqls)


def get_ip(ip_str):
    '''
    获取 ip
    Args:
        ip_str:

    Returns:

    '''
    host = ()
    pos1 = 0
    pos2 = 0
    pos3 = 0
    if "running" in ip_str:
        pos1 = ip_str.find(" ")
        pos2 = ip_str.find(" ", pos1 + 1)
        pos3 = ip_str.find("running")
        name = ip_str[pos2: pos3].strip()
        host = (name, "running")
    if "shut off" in ip_str:
        pos1 = ip_str.find(" ")
        pos2 = ip_str.find(" ", pos1 + 1)
        pos3 = ip_str.find("shut off")
        name = ip_str[pos2: pos3].strip()
        host = (name, "shut off")

    print host


def get_ip1(ip_str):
    '''
    获取 ip
    Args:
        ip_str:

    Returns:

    '''
    host = ()
    pos1 = 0
    pos2 = 0
    if "centos" in ip_str:
        if "running" in ip_str:
            if "|" in ip_str:
                pos1 = ip_str.find("|")
                pos2 = ip_str.find("|", pos1 + 1)
            elif ":" in ip_str:
                pos1 = ip_str.find(":")
                pos2 = ip_str.find(":", pos1 + 1)

            host = (ip_str[pos1 + 1:pos2], "running")

        if "shut off" in ip_str:
            if "|" in ip_str:
                pos1 = ip_str.find("|")
                pos2 = ip_str.find("|", pos1 + 1)
            elif ":" in ip_str:
                pos1 = ip_str.find(":")
                pos2 = ip_str.find(":", pos1 + 1)

            host = (ip_str[pos1 + 1:pos2], "shut off")

    return host


def test_update(lists):
    query_sql = ""
    delete_sql = ""
    insert_sql = ""
    try:
        for tup in lists:
            physical_ip = tup[0]
            vm_ip = tup[1]
            vm_status = tup[2]
            ops_mysql = OpsMysql()
            query_sql = """ select `cabinet`, `physical_sn` from `server_info` where `physical_ip` = %s """ % (
                physical_ip,)
            delete_sql = """ delete from `server_info` where `physical_ip` = %s  """ % (physical_ip,)

            query_result = ops_mysql.query(query_sql)

            ops_mysql.update(delete_sql)

            insert_sql = """ insert into `server_info`(`cabinet`, `physical_sn`, `physical_ip`, `vm_ip`, `vm_status`) values(%s, %s, %s, %s, %s) """ % (
                query_result["cabinet"], query_result["physical_sn"], physical_ip, vm_ip, vm_status)

            ops_mysql.update(insert_sql)

    except Exception as e:
        e


def read_file(path):
    with io.open(path, "r") as file:
        lists = []
        physical_ip = ""
        try:
            datas = file.readlines()
            msg = datas[0].split(" ")
            physical_ip = msg[1]
            flag = msg[2].encode('utf-8')
            if "True" in flag:
                for data in datas[1:]:
                    if "running" in data:
                        arr = data.split(" ")
                        if len(arr) > 1 and ("10." in arr[1] or "192." in arr[1]):
                            vm_ip = arr[1].replace("\n", "")
                            vm_status = arr[0]
                            lists.append((physical_ip, vm_ip, vm_status))

                        # else:
                        #     print " running 有虚拟机但无 ip  " + physical_ip
                    elif "shut off" in data:
                        arr = data.split(" ")
                        if len(arr) > 2 and ("10." in arr[2] or "192." in arr[2]):
                            vm_ip = arr[2].replace("\n", "")
                            vm_status = arr[0] + " " + arr[1]
                            lists.append((physical_ip, vm_ip, vm_status))
                        # else:
                        #     print " shut off 有虚拟机但无 ip  " + physical_ip


        except Exception as e:
            print e
            print " ========== " + path

        if len(lists) > 0:
            test_update(lists)
            # print lists

        return lists


def traverse():
    dirname = "/Users/jixuzhang/Desktop/data/test/data/info"
    # 所有的文件
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        # 当前主目录
        # print("1:", maindir)
        # 当前主目录下的所有目录
        # print("2:", subdir)
        # 当前主目录下的所有文件
        # print("3:", file_name_list)

        for filename in file_name_list:
            # 合并成一个完整路径
            apath = os.path.join(maindir, filename)
            result.append(apath)

    for path in result:
        read_file(path)


def test_io():
    list_file = ["1-4B-K06", "1-4B-L02", "1-4B-M11", "1-4B-M13", "1-4B-P01", "1-4B-K07", "1-4B-L08", "1-4B-M12",
                 "1-4B-O01"]
    for cabinet in list_file:
        with io.open("/Users/jixuzhang/Desktop/data/test/data/cabinet/" + cabinet + ".txt", "r") as file:
            arr = []
            for data in file.readlines():
                arrs = data.split("\t")
                physical_sn = arrs[0]
                physical_ip = arrs[1].replace("\n", "")
                # arr.append((cabinet, physical_sn, physical_ip))
                get_avaliable_connection(cabinet, physical_sn, physical_ip)


def test_mysql():
    query_sql = """ select `cabinet`, `physical_sn` from `server_info` where `physical_ip` = %s """ % ("",)


if __name__ == '__main__':
    test_io()
    print "success"
