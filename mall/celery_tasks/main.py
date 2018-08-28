# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: Robinson_Jim
# @time: 18-8-21 下午7:16

from celery import Celery

# 进行celery允许配置
# 为celery使用django配置文件进行配置
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'

"""此文件作为启动celery的主文件"""
app = Celery('celery_tasks')  # 括号里面传入脚本路径

# 加载配置文件
app.config_from_object('celery_tasks.config')

# 自动加载识别任务:
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.mail'])
