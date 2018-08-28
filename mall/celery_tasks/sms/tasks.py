# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author: Robinson_Jim
# @time: 18-8-21 下午7:16
from celery_tasks.main import app
from libs.yuntongxun.sms import CCP


@app.task(name='xxxx')
def send_sms_code(mobile, sms_code):
    ccp = CCP()
    ccp.send_template_sms(mobile, [sms_code, 60 * 5], 1)
