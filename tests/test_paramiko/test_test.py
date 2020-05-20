# -*- coding: utf-8 -*-
import paramiko
import re


def ssh_virsh():
    password2 = "PS123abc,."
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.76.1.3', username='psadmin', password='PS123abc,.')

    # Get the List of files
    # stdin, stdout, stderr = ssh.exec_command("sudo virsh  list --all --title", get_pty=True)
    stdin, stdout, stderr = ssh.exec_command("sudo virsh  list --all", get_pty=True)
    stdin.write(password2 + "\n")
    stdout_list = stdout.read().decode(encoding="utf-8").split("\n")
    # print len(stdout_list)
    for vm_len in range(4, len(stdout_list) - 2):
        vm_info = stdout_list[vm_len]
        # print vm_info
        # vm_name = split_str(vm_info)[1]
        vm_name = "vm_name"
        print vm_name

        exec_command_vm_status = "sudo virsh domstate " + vm_name
        exec_command_vm_cpu = "sudo virsh vcpucount --current " + vm_name + " --live"
        exec_command_vm_memory = "sudo virsh dominfo " + vm_name + " | grep -i \"Max memory\" "

        # how to get disk info
        exec_command_vm_disk = " "

        vm_status_stdin, vm_status_stdout, vm_status_stderr = ssh.exec_command(exec_command_vm_status, get_pty=True)
        vm_cpu_stdin, vm_cpu_stdout, vm_cpu_stderr = ssh.exec_command(exec_command_vm_cpu, get_pty=True)
        vm_memory_stdin, vm_memor_stdout, vm_memor_stderr = ssh.exec_command(exec_command_vm_memory, get_pty=True)
        vm_cpu_stdin.write(password2 + "\n")
        vm_status_stdin.write(password2 + "\n")
        vm_memory_stdin.write(password2 + "\n")

        vm_memory = vm_memor_stdout.read().decode(encoding="utf-8")
        pattern = re.compile(r'\d+')  # 查找数字
        result_vm_memory = pattern.findall(vm_memory)

        print(vm_cpu_stdout.read().decode(encoding="utf-8"))
        print(vm_status_stdout.read().decode(encoding="utf-8"))
        print(result_vm_memory)
        # print(vm_memory)
        print("************")

    print "********"


if __name__ == '__main__':
    print 4194304 / 1024 / 1024
