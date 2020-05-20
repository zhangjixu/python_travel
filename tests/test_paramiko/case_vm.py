# -*- coding: utf-8 -*-
import paramiko
from tests.test_io import io_utils

user = 'centos'
passwords = ['centospshl2016', 'centosps2016']


def get_vm_machine_info(master_host, host):
    '''
    获取虚拟机信息
    Args:
        master_host:
        host:

    Returns:

    '''
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 验证密码是否正确
        flag = False
        for password in passwords:
            try:
                ssh.connect(host, 22, user, password)
                flag = True
                break
            except Exception:
                continue

        if flag:
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
            fdisk_stdin, fdisk_stdout, fdisk_stderr = ssh.exec_command('sudo fdisk -l | grep -i Disk', get_pty=True)
            fdisk_stdin.write(password + "\n")
            fdisks = "磁盘大小 fdisk -l: \n" + fdisk_stdout.read().decode('utf-8')

            folder_path = "/Users/jixuzhang/Desktop/data/test/data/ip/vm_ip/" + master_host
            # 创建文件夹
            io_utils.create_folder(folder_path)
            path = "/Users/jixuzhang/Desktop/data/test/data/ip/vm_ip/" + master_host + "/" + host + ".txt"
            io_utils.save_file(path, cpus)
            io_utils.save_file(path, mems)
            io_utils.save_file(path, dfs)
            io_utils.save_file(path, fdisks)
        else:
            print "密码不对 主机 ip : " + master_host + " 虚拟机 ip 为: " + host


    except Exception as e:
        print e, " ==================== 主机 ip 为 : " + master_host + " 虚拟机 ip 为: " + host
    finally:
        ssh.close()


def get_vm_machine_info1(master_host, host):
    '''
    获取虚拟机信息
    Args:
        master_host:
        host:

    Returns:

    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 验证密码是否正确
    flag = False
    real_pwd = ''
    for password in passwords:
        try:
            ssh.connect(host, 22, user, password)
            flag = True

            break
        except Exception:
            continue

    if flag:
        # 获取虚拟机 cpu 信息
        cpu_stdin, cpu_stdout, cpu_stderr = ssh.exec_command('cat /proc/cpuinfo| grep "processor"| wc -l')
        cpus = "cpu 核数: " + cpu_stdout.read().decode('utf-8')

        # 获取虚拟机内存信息
        mem_stdin, mem_stdout, mem_stderr = ssh.exec_command('free -m | grep -i  Mem')
        mems = "内存大小: " + mem_stdout.read().decode('utf-8')

        # 获取虚拟机磁盘信息
        df_stdin, df_stdout, df_stderr = ssh.exec_command('df -h')
        dfs = "磁盘大小 df -h: " + df_stdout.read().decode('utf-8')

        # 获取物理机磁盘信息
        fdisk_stdin, fdisk_stdout, fdisk_stderr = ssh.exec_command('sudo fdisk -l | grep -i Disk', get_pty=True)
        fdisk_stdin.write(password + "\n")
        fdisks = "磁盘大小 fdisk -l: " + fdisk_stdout.read().decode('utf-8')

        folder_path = "/Users/jixuzhang/Desktop/data/test/data/ip/vm_ip/" + master_host
        # 创建文件夹
        io_utils.create_folder(folder_path)
        path = "/Users/jixuzhang/Desktop/data/test/data/ip/vm_ip/" + master_host + "/" + host + ".txt"
        io_utils.save_file(path, cpus)
        io_utils.save_file(path, mems)
        io_utils.save_file(path, dfs)
        io_utils.save_file(path, fdisks)
    else:
        print "密码不对 主机 ip : " + master_host + " 虚拟机 ip 为: " + host


def array_vm_ip(json):
    master_ip = json["master_ip"]
    ips = json["ips"]
    for ip in ips:
        get_vm_machine_info(master_ip, ip)


if __name__ == '__main__':
    json = {"master_ip": "10.76.1.3", "ips": ["10.76.83.92"]}
    # json = {"master_ip": "10.76.1.4", "ips": ["10.76.83.100", "10.76.83.101", "10.76.23.56"]}
    array_vm_ip(json)
