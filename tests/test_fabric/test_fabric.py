# -*- coding: utf-8 -*-

import fabric
from fabric.api import *
from fabric.contrib.console import confirm

password = 'centosps2016'
env.user = 'centos'
env.hosts = ['192.168.20.151', '192.168.20.152']
# 输入密码的时候记得带上 端口号
env.passwords = {'centos@192.168.20.151:22': password, 'centos@192.168.20.152:22': password}
# 分组操作
env.roledefs = {'download': ['192.168.20.152'], 'upload': ['192.168.20.151'], 'user': ['192.168.20.151']}


@task
@roles('download')
def test():
    '''
    切换目录操作
    下载文件到本地
    上传文件
    :return:
    '''
    run('uname -s')
    run('id -un')
    with cd('data'):
        run('more 2018-11-19_countAPITime.log  | grep \'querySolr nm:石博 AND idcd:142732199110276810\'')
        # 下载文件到本地
        get('2018-11-19_countAPITime.log', '/Users/jixuzhang/Desktop/data')
        # 上传文件到远程
        put('/Users/jixuzhang/Desktop/data/sql.log', '/home/centos/data')


@task
@roles('upload')
def test_role_upload():
    run('echo upload')


@task
@roles('download')
def test_role_download():
    run('ifconfig')


@task
@roles('download')
def test_su():
    sudo('sudo su - java')
    run('id -un')


@task
@roles('user')
def test_exception():
    with cd('/home/centos/data'):
        # warn_only=True 遇到错误，还会继续执行后面的语句
        with settings(warn_only=True):
            result = run('more data.txt | grep \"as\"')
            print fabric.colors.red('执行是否成功: ' + str(not result.failed), bold=False)
            print fabric.colors.cyan('执行的结果为: ' + str(result.stdout), bold=False)
            print fabric.colors.yellow('返回结果类型: ' + str(type(result.stdout)), bold=False)
            if result.failed:
                # 即使 warn_only 设置成 True，捕捉到错误之后，还是退出
                abort('退出')


@task
@roles('user')
def test_data():
    with cd('/home/centos/data'):
        # 使用 prompt 函数获取用户输入的字符串
        content = prompt('请输入字符串:')
        print fabric.colors.red(content, bold=False)
        # confirm 用于输入 y or n 确认是否继续
        content2 = confirm('请确认?')
        print fabric.colors.red(content2, bold=False)

        # 通过local来执行任务，需要通过capture＝True来得到值
        with settings(warn_only=True):
            with lcd('/Users/jixuzhang/Desktop/data'):
                result = local('more test.sql | grep 1', capture=True)
                print fabric.colors.yellow('返回结果为: ' + str(result.stdout), bold=False)
