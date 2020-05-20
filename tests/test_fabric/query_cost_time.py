# -*- coding: utf-8 -*-

import fabric
from fabric.api import *

password = 'java'
env.user = 'java'
env.hosts = ['10.76.85.201', '10.76.85.202', '10.76.85.203', '10.76.85.204', '10.76.85.205']
# 输入密码的时候记得带上 端口号
env.passwords = {'java@10.76.85.201:22': password, 'java@10.76.85.202:22': password, 'java@10.76.85.203:22': password,
                 'java@10.76.85.204:22': password, 'java@10.76.85.205:22': password}
# 分组操作
env.roledefs = {'java': ['10.76.85.201', '10.76.85.202', '10.76.85.203', '10.76.85.204', '10.76.85.205']}


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
