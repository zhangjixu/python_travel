# -*- coding: utf-8 -*-

import io
import sys
import paramiko
from module.OpsMysql import OpsMysql

reload(sys)
sys.setdefaultencoding('utf-8')

ops_mysql = OpsMysql()


def get_avaliable_connection(cabinet, physical_sn, physical_ip):
    '''
    获取可用的连接
    Args:
        host:

    Returns:

    '''
    available = {"psadmin": "", "root": "", "root_second": ""}
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

        # 获取物理机的 cpu 核数
        phy_cpu_stdin, phy_cpu_stdout, phy_cpu_stderr = ssh.exec_command(
            'cat /proc/cpuinfo| grep "processor"| wc -l')
        phy_cpu = phy_cpu_stdout.read().decode(encoding="utf-8")

        # 获取物理机内存
        phy_memory_stdin, phy_memory_stdout, phy_memory_stderr = ssh.exec_command(
            " cat /proc/meminfo  | grep -i MemTotal")
        phy_memory_str = phy_memory_stdout.read().decode(encoding="utf-8")
        phy_memory = get_phy_memory(phy_memory_str)

        # 获取物理机虚拟机信息
        vm_stdin, vm_stdout, vm_stderr = ssh.exec_command('sudo virsh list --all --title', get_pty=True)
        vm_stdin.write(password + "\n")
        result_vm = vm_stdout.read().decode('utf-8')
        stdin, stdout, stderr = ssh.exec_command('sudo virsh list --all --title', get_pty=True)

        # 判断物理机是否有虚拟机
        if "command not found" not in result_vm:
            for vm in stdout:
                get_ip_result = get_ip(vm)

                # 判断是否存在虚拟机
                if len(get_ip_result) > 0:
                    hostname, vm_status = get_ip_result

                    # 判断虚拟机是否开启
                    if "running" in vm_status:
                        vm_memory = get_vm_memory(ssh, password, hostname)
                        vm_cpu = get_vm_cpu(ssh, password, hostname)
                        sql = """ insert into `server_info`(`cabinet`, `phy_sn`, `phy_ip`, `phy_cpu`, `phy_memory`, `hostname`, `vm_status`, `vm_cpu`, `vm_memory`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                        ops_mysql.update(sql, (
                            cabinet, physical_sn, physical_ip, phy_cpu, phy_memory, hostname, vm_status, vm_cpu,
                            vm_memory))
                    else:
                        sql = """ insert into `server_info`(`cabinet`, `phy_sn`, `phy_ip`, `phy_cpu`, `phy_memory`, `hostname`, `vm_status`) values(%s, %s, %s, %s, %s, %s, %s) """
                        ops_mysql.update(sql,
                                         (cabinet, physical_sn, physical_ip, phy_cpu, phy_memory, hostname, vm_status))

        # 此物理机无虚拟机
        else:
            sql = """ insert into `server_info`(`cabinet`, `phy_sn`, `phy_ip`, `phy_cpu`, `phy_memory`) values(%s, %s, %s, %s, %s) """
            ops_mysql.update(sql, (cabinet, physical_sn, physical_ip, phy_cpu, phy_memory))


    except Exception as e:
        print e.message
    finally:
        ssh.close()


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

    return host


def get_phy_memory(phy_memory_stdout):
    '''
    获取物理机内存
    Args:
        phy_memory_stdout:

    Returns:

    '''
    pos1 = phy_memory_stdout.find(":") + 1
    pos2 = phy_memory_stdout.find("KB") - 2
    phy_memory = int(phy_memory_stdout[pos1:pos2].strip()) / 1024 / 1024
    return str(phy_memory) + "GB"


def get_vm_memory(ssh, password, hostname):
    '''
    获取虚拟机内存
    Args:
        ssh:
        password:
        hostname:

    Returns:

    '''
    exec_command_vm_memory = "sudo virsh dominfo " + hostname + " | grep -i \"Max memory\" "
    stdin, stdout, stderr = ssh.exec_command(exec_command_vm_memory, get_pty=True)
    stdin.write(password + "\n")
    vm_memory = stdout.read().decode(encoding="utf-8")
    pos1 = vm_memory.find(":") + 1
    pos2 = vm_memory.find("KiB")
    memory_str = vm_memory[pos1: pos2].strip()
    memory = int(memory_str) / 1024 / 1024
    return str(memory) + "GB"


def get_vm_cpu(ssh, password, hostname):
    '''
    获取虚拟机 cpu 核数
    Args:
        ssh:
        password:
        hostname:

    Returns:

    '''
    exec_command_vm_cpu = "sudo virsh dominfo " + hostname + " | grep -i \"CPU(s):\" "
    stdin, stdout, stderr = ssh.exec_command(exec_command_vm_cpu, get_pty=True)
    stdin.write(password + "\n")
    vm_memory = stdout.read().decode(encoding="utf-8")
    pos1 = vm_memory.find(":") + 1
    cpu = vm_memory[pos1:].strip()
    return cpu


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
                # print cabinet, physical_sn, physical_ip


if __name__ == '__main__':
    # 10.76.2.7
    test_io()
    print "success"
