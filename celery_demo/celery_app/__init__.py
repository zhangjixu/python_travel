# -*- coding: utf-8 -*-
from celery import Celery

# 创建 Celery 实例
app = Celery('test_celery')

# 通过 Celery 实例加载配置模块
app.config_from_object('celery_demo.celery_app.celeryconfig')

if __name__ == "__main__":
     app.start()
