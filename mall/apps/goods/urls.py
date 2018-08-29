# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Robinson_Jim
# @time: 18-8-29 下午7:37

from django.conf.urls import url
from . import views

urlpatterns = [
    #/goods/categories/
    url(r'^categories/$',views.CategoryView.as_view(),name='cagegories'),
]