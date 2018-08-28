# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: Robinson_Jim
# @time: 18-8-27 上午11:31
from rest_framework.routers import DefaultRouter
from .views import AreasView

urlpatterns = [

]

router = DefaultRouter()
router.register(r'infos', AreasView, base_name='area')

urlpatterns += router.urls
