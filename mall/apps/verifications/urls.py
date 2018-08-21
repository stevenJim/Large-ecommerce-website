# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Robinson_Jim
# @time: 18-8-21 下午2:53
from django.conf.urls import url
from . import views

urlpatterns=[
    # /verifications/imagecodes/(?P<image_code_id>.+)/
    url(r'^imagecodes/(?P<image_code_id>.+)/$',views.ImageCodeView.as_view(),name='imagecodes'),
    url(r'^smscodes/(?P<mobile>1[345789]\d{9})/$',views.SmsCodeView.as_view(),name='smscodes')

]