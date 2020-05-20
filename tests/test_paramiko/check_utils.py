# -*- coding: utf-8 -*-

import paramiko
import io
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

from tests.test_io import io_utils


# user = 'root'
# password = '123abc,.'


def check_true(host, sn):
    user = 'psadmin'
    password = 'PS123abc,.'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, user, password)
    # stdin, stdout, stderr = ssh.exec_command(""" . ./.bash_profile; echo $PATH """, get_pty=True)
    stdin, stdout, stderr = ssh.exec_command(""" cat /proc/cpuinfo| grep "processor"| wc -l """, get_pty=True)
    stdin.write(password + "\n")
    print_sn = stdout.read().decode('utf-8')
    print print_sn
    ssh.close()


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

    # get_physical_machine_info(ssh, host, password)

    get_phy_memory(ssh, host, password)


def get_avaliable_connection1(host):
    '''
    获取可用的连接
    Args:
        host:

    Returns:

    '''
    available = {"psadmin": "PS123abc,.", "root": "123abc,.", "root_second": "ps123abc,."}
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 判断是否登录成功
    flag = False
    for user, password in available.items():
        try:
            ssh.connect(host, 22, user.replace("root_second", "root"), password)
            stdin, stdout, stderr = ssh.exec_command(""" date """, get_pty=True)
            # stdout.read().decode('utf-8')
            flag = True
            break
        except Exception as e:
            continue

    if not flag:
        print host


def get_physical_machine_info(ssh, host, password):
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

        vm_ip_str = ''
        flag = False
        if "command not found" not in result_vm:
            flag = True
            for vm in stdout:
                count_ip += 1
                get_ip_result = get_ip(vm)
                if len(get_ip_result) > 0:
                    vm_ip_str += get_ip_result[1] + " " + get_ip_result[0] + "\n"

        path = "/Users/jixuzhang/Desktop/data/test/data/info/" + host + ".txt"
        io_utils.save_file(path, "physical_ip: " + host + " " + str(flag))
        io_utils.save_file(path, vm_ip_str)

    except Exception as e:
        print e

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


def test_split():
    with io.open("/Users/jixuzhang/Desktop/data/test/ip.txt", "r") as file:
        arr = []
        for data in file.readlines():
            arrs = data.split(" ")
            arr.append(arrs[1].replace("\n", ""))

        return arr


def array_machine(arr_host):
    '''
    遍历数组中的物理机 ip
    Args:
        arr_host:

    Returns:

    '''
    for host in arr_host:
        get_avaliable_connection(host)


def test_pa(ssh, host, password):
    exec_command_vm_memory = "sudo virsh dominfo v3s-mysql-13.204 | grep -i \"Max memory\" "
    stdin, stdout, stderr = ssh.exec_command(exec_command_vm_memory, get_pty=True)
    stdin.write(password + "\n")
    vm_memory = stdout.read().decode(encoding="utf-8")
    pos1 = vm_memory.find(":") + 1
    pos2 = vm_memory.find("KiB")
    memory_str = vm_memory[pos1: pos2].strip()
    memory = int(memory_str) / 1024 / 1024
    print memory


def test_pa1(ssh, host, password):
    exec_command_cpu = """ cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l """
    stdin, stdout, stderr = ssh.exec_command(exec_command_cpu)
    # stdin.write(password + "\n")
    cpu = stdout.read().decode(encoding="utf-8")

    print cpu


def get_vm_cpu(ssh, host, password):
    exec_command_vm_cpu = "sudo virsh dominfo v3s-mysql-13.204 | grep -i \"CPU(s):\" "
    stdin, stdout, stderr = ssh.exec_command(exec_command_vm_cpu, get_pty=True)
    stdin.write(password + "\n")
    vm_memory = stdout.read().decode(encoding="utf-8")
    pos1 = vm_memory.find(":") + 1
    cpu = vm_memory[pos1:].strip()
    print cpu


def get_phy_memory(ssh, host, password):
    exec_command_vm_cpu = "cat /proc/meminfo  | grep -i MemTotal "
    stdin, phy_memory_stdout, stderr = ssh.exec_command(exec_command_vm_cpu)
    phy_memory_str = phy_memory_stdout.read().decode(encoding="utf-8")
    pos1 = phy_memory_str.find(":") + 1
    pos2 = phy_memory_str.find("KB") - 2
    result = phy_memory_str[pos1:pos2].strip()
    print result
    # phy_memory = int(result) / 1024 / 1024
    # return str(phy_memory) + "GB"


if __name__ == '__main__':
    # check_true("10.76.1.3", "GHY91L2")
    # get_avaliable_connection("10.76.88.72")
    # arrs = test_split()
    # arrs = ['10.76.1.3']
    # array_machine(arrs)
    get_avaliable_connection("10.76.1.3")
    print " ========= success ========= "
