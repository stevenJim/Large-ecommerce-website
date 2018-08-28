# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author: Robinson_Jim
# @time: 18-8-26 下午6:44
from django.core.mail import send_mail
from mall import settings
from celery_tasks.main import app


@app.task(name='send_verify_mail')
def send_verify_mail(to_email, verify_url):
    """发送验证邮箱邮件:
    subject, 邮件主题
    message, 邮件文本,一般不用二用html_message
    from_email, 从那个邮件发出,
    recipient_list, 收件人列表
    html_message=None ,邮件内荣一般带有html格式
    """
    subject = '美多商城邮箱验证'
    message = ''
    from_email = settings.EMAIL_FROM
    recipient_list = [to_email]
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
