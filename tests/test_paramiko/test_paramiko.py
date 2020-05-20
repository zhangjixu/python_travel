# -*- coding: utf-8 -*-

import paramiko

user = 'centos'
password = ['centospshl2016', 'centosps2016']

phy_user = 'psadmin'
phy_pwd = 'PS123abc,.'


def test(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    flag = False
    for pwd in password:
        try:
            ssh.connect(host, 22, user, pwd)
            flag = True
            break
        except Exception as e:
            continue

    if flag:
        stdin, stdout, stderr = ssh.exec_command('date')
        result = stdout.read().decode('utf-8')
        print type(result)

    ssh.close()


def test2():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.76.1.3", 22, phy_user, phy_pwd)
    vm_ip_stdin, vm_ip_stdout, vm_ip_stderr = ssh.exec_command('sudo virsh list --all --title', get_pty=True)
    vm_ip_stdin.write(phy_pwd + "\n")
    result = vm_ip_stdout.read().decode('utf-8')
    print type(result), result

    ssh.close()


def test1():
    num = "c"
    if num!= 'c' :
        print 1


if __name__ == '__main__':
    # test("10.76.11.73")
    test1()
