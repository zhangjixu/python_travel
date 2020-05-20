# -*- coding: utf-8 -*-

# 指定 Broker
BROKER_URL = 'redis://192.168.11.230:6379/1'

# 指定 Backend
CELERY_RESULT_BACKEND = 'redis://192.168.11.230:6379/2'

# 指定时区，默认是 UTC
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_ACCEPT_CONTENT = ['json']

# 指定导入的任务模块
CELERY_IMPORTS = (
    'celery_demo.celery_app.task1',
    'celery_demo.celery_app.task2'
)
