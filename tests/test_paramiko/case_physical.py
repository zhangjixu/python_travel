# -*- coding: utf-8 -*-

import paramiko
import io
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from tests.test_paramiko import case_vm
from tests.test_io import io_utils

user = 'psadmin'
password = 'PS123abc,.'


def get_physical_machine_info(ssh, host, password):
    '''
    获取物理机信息
    Args:
        host:

    Returns:

    '''
    try:

        # 获取虚拟机 cpu 信息
        cpu_stdin, cpu_stdout, cpu_stderr = ssh.exec_command('cat /proc/cpuinfo| grep "processor"| wc -l')
        cpus = "cpu 核数: \n" + cpu_stdout.read().decode('utf-8')

        # 获取虚拟机内存信息
        mem_stdin, mem_stdout, mem_stderr = ssh.exec_command('free -m | grep -i  Mem')
        mems = "内存大小: \n" + mem_stdout.read().decode('utf-8')

        # 获取虚拟机磁盘信息
        df_stdin, df_stdout, df_stderr = ssh.exec_command('df -h')
        dfs = "磁盘大小 df -h: \n" + df_stdout.read().decode('utf-8')

        # 获取物理机磁盘信息
        fdisk_stdin, fdisk_stdout, fdisk_stderr = ssh.exec_command('sudo fdisk -l', get_pty=True)
        fdisk_stdin.write(password + "\n")
        fdisks = "磁盘大小 fdisk -l: \n" + fdisk_stdout.read().decode('utf-8')

        # 获取物理机虚拟机信息
        vm_stdin, vm_stdout, vm_stderr = ssh.exec_command('sudo virsh list --all --title', get_pty=True)
        vm_stdin.write(password + "\n")
        result_vm = vm_stdout.read().decode('utf-8')

        # 统计虚拟机 ip 数量
        count_ip = 0

        # 虚拟机 ip
        vm_ip_str = ''
        # 判断物理机是否有虚拟机
        if "command not found" not in result_vm:
            vm_stdin, vm_stdout, vm_stderr = ssh.exec_command('sudo virsh list --all --title', get_pty=True)
            vm_stdin.write(password + "\n")
            vms = "vm: "

            ip_num = 0
            for vm in vm_stdout:
                count_ip += 1
                vms = vms + vm + "\n"
                get_ip_result = get_ip(vm)
                if get_ip_result != '':
                    ip_num += 1
                    vm_ip_str += str(ip_num) + "  " + get_ip_result + "\n"

            count_ip -= 5

            # 获取物理机虚拟机 ip 信息
            vm_ip_stdin, vm_ip_stdout, vm_ip_stderr = ssh.exec_command(
                'sudo virsh list --all --title | grep -i running',
                get_pty=True)
            vm_ip_stdin.write(password + "\n")

            for ip in vm_ip_stdout:
                try:
                    get_vm_ip(host, ip)
                except Exception as e:
                    print "get_vm_ip exception: " + e.message
                    continue
        else:
            result_vm = "此物理机无虚拟机"

        path = "/Users/jixuzhang/Desktop/data/test/data/ip/physical_ip/" + host + ".txt"
        io_utils.save_file(path, cpus)
        io_utils.save_file(path, mems)
        io_utils.save_file(path, dfs)
        io_utils.save_file(path, fdisks)
        io_utils.save_file(path, "=========== ip size: " + str(count_ip) + "\n" + result_vm + "\n")
        io_utils.save_file(path, "ip 数量如下: \n" + vm_ip_str)

    except Exception as e:
        print e
        print host + " 获取物理机信息出现异常: " + e.message
    finally:
        ssh.close()


def array_machine(arr_host):
    '''
    遍历数组中的物理机 ip
    Args:
        arr_host:

    Returns:

    '''
    for host in arr_host:
        get_avaliable_connection(host)
        print "\n"


def get_avaliable_connection(host):
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
            ssh.connect(host, 22, user.replace("root_second", "root"), password)
            break
        except Exception:
            continue

    get_physical_machine_info(ssh, host, password)


def get_ip(ip_str):
    '''
    获取 ip
    Args:
        ip_str:

    Returns:

    '''
    host = ''
    pos1 = 0
    pos2 = 0
    if "running" in ip_str:
        if "|" in ip_str:
            pos1 = ip_str.find("|")
            pos2 = ip_str.find("|", pos1 + 1)
        elif ":" in ip_str:
            pos1 = ip_str.find(":")
            pos2 = ip_str.find(":", pos1 + 1)

        host = "running   " + ip_str[pos1 + 1:pos2]

    if "shut off" in ip_str:
        if "|" in ip_str:
            pos1 = ip_str.find("|")
            pos2 = ip_str.find("|", pos1 + 1)
        elif ":" in ip_str:
            pos1 = ip_str.find(":")
            pos2 = ip_str.find(":", pos1 + 1)

        host = "shut off   " + ip_str[pos1 + 1:pos2]

    return host


def get_vm_ip(master_host, ip_str):
    '''
    获取虚拟机信息
    Args:
        master_host:
        ip_str:

    Returns:

    '''
    if "running" in ip_str:
        if "|" in ip_str:
            pos1 = ip_str.find("|")
            pos2 = ip_str.find("|", pos1 + 1)
            host = ip_str[pos1 + 1:pos2]
            case_vm.get_vm_machine_info(master_host, host)
        elif ":" in ip_str:
            pos1 = ip_str.find(":")
            pos2 = ip_str.find(":", pos1 + 1)
            host = ip_str[pos1 + 1:pos2]
            case_vm.get_vm_machine_info(master_host, host)


def check_true(host, sn):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, user, password)
    stdin, stdout, stderr = ssh.exec_command(""" dmidecode -t system | grep 'Serial Number' | awk -F: '{print $2}' """)
    stdout.read().decode('utf-8')


def test_split():
    with io.open("/Users/jixuzhang/Desktop/data/test/ip.txt", "r") as file:
        arr = []
        for data in file.readlines():
            arrs = data.split(" ")
            arr.append(arrs[1].replace("\n", ""))

        return arr


if __name__ == '__main__':
    # arr_host = ['10.76.1.3', '10.76.88.72']
    arr_host = test_split()
    # print arr_host
    array_machine(arr_host)
    print "success"
