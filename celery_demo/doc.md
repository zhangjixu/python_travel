#### 启动 celery
```angular2html
在 celery_demo 目录上一层执行以下命令
celery -A celery_demo.celery_app worker -l=info
参数 -A 指定了 Celery 实例的位置

```