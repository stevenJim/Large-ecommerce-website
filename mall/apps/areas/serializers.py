# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: Robinson_Jim
# @time: 18-8-26 下午8:25

from rest_framework import serializers
from .models import Area


class AreasSerializer(serializers.ModelSerializer):
    """
    行政区划信息序列化器
    """

    class Meta:
        model = Area
        fields = ('id', 'name', 'parent_id')


class SubAreasSerializer(serializers.ModelSerializer):
    """
    子行政区划信息序列化器
    """
    subs = AreasSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id','name','subs']
