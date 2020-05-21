# -*- coding: utf-8 -*-

import fabric
from fabric.api import *

password = 'java'
env.user = 'java'
env.hosts = ['']
# 输入密码的时候记得带上 端口号
env.passwords = {'java@': password}
# 分组操作
env.roledefs = {'java': ['']}


@task
def cost_time():
    with cd('/usr/local/tomcat8/logs/countTime'):
        with settings(warn_only=True):
            result = run('more countTime.log |  egrep \'共用时 [3-9]{2,6}}* ms\' | egrep -v \'sn/queryBatchByPhone\'')
            # 如果执行没有结果，会认为是执行失败
            if result.failed:
                print fabric.colors.red('执行无结果')
            else:
                print fabric.colors.green('执行结果为: ' + str(result.stdout))
