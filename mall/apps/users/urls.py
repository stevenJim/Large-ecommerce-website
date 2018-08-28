# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Robinson_Jim
# @time: 18-8-21 下午1:09
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # /users/usernames/(?P<username>\w{5,20})/count/t
    url(r'usernames/(?P<username>\w{5,20})/count/', views.UsernameView.as_view(), name='username'),
    url(r'phones/(?P<mobile>1[345789]\d{9})/count/', views.PhoneView.as_view(), name='phone'),
    url(r'^$', views.RegisterSubmitView.as_view(), name='register'),
    #     Django REST framework JWT提供了登录获取token的视图，可以直接使用,在users应用中的urls添加路由信息
    url(r'auths/', obtain_jwt_token, name='auths'),
    url(r'^infos/$', views.UserCenterView.as_view(), name='detail'),
    url(r'^emails/$', views.EmailView.as_view(), name='send_mail'),
    url(r'^emails/verification/$', views.VerifyEmailView.as_view(), name='verify_mail'),
]

from .views import AddressView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'addresses', AddressView, base_name='address')
urlpatterns += router.urls
