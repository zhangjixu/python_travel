# -*- coding: utf-8 -*-

import io
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from fabric.api import env, sudo, task, run

env.user = 'psadmin'
env.password = 'PS123abc,.'
env.sudo_password = env.password
env.hosts = ['10.76.1.3']
env.port = 22


def save_file(path, content):
    '''
    保存数据到指定路径
    Args:
        path: 文件路径
        content: 保存内容

    Returns:

    '''
    with io.open(path, 'a+', encoding='utf-8') as file:
        content = str(content) + u'\n'
        file.write(content)


@task
def default():
    ip = run(""" ifconfig | grep -i 10.76. """)
    ip_str = ip.stdout
    print ip_str


def get_ip(ip_str):
    pos1 = ip_str.index("inet") + 4
    pos2 = ip_str.index("netmask")
    return ip_str[pos1:pos2].strip()


@task
def default1():
    ip = run(""" ifconfig | grep -i 10.76. """)
    ip_str = ip.stdout
    real_ip = get_ip(ip_str)
    path = "/Users/jixuzhang/Desktop/data/test/data/ip/" + real_ip + ".txt"

    core = "cpu core: " + run(""" cat /proc/cpuinfo| grep "processor"| wc -l """).stdout + "\n"
    mem = "memory: " + run(""" free -m | grep -i  Mem """).stdout + "\n"
    df = "df -h: " + run(""" df -h """).stdout + "\n"
    fdisk = "fdisk: " + sudo(""" fdisk -l | grep -i Disk """).stdout + "\n"
    vm = sudo(""" virsh list --all --title """).stdout + "\n"
    save_file(path, core)
    save_file(path, mem)
    save_file(path, df)
    save_file(path, fdisk)
    save_file(path, vm)
    # print core.stdout, mem.stdout, df.stdout, fdisk.stdout, vm.stdout
    # test()


def host():
    core = run(""" cat /proc/cpuinfo| grep "processor"| wc -l """)
    mem = run(""" free -m | grep -i  Mem """)
    df = run(""" df -h """)
    fdisk = sudo(""" fdisk -l | grep -i Disk """)
    vm = sudo(""" virsh list --all --title """)
    print core.stdout, mem.stdout, df.stdout, fdisk.stdout, vm.stdout


def test():
    print " ================================ "


if __name__ == '__main__':
    default()
