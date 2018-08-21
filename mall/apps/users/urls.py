# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Robinson_Jim
# @time: 18-8-21 下午1:09
from django.conf.urls import url
from . import views

urlpatterns = [
    # /users/usernames/(?P<username>\w{5,20})/count/t
    url(r'usernames/(?P<username>\w{5,20})/count/',views.UsernameView.as_view(),name='username'),
    url(r'phones/(?P<mobile>1[345789]\d{9})/count/',views.PhoneView.as_view(),name='phone'),

]
