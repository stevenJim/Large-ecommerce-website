# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: Robinson_Jim
# @time: 18-8-21 下午3:40
from redis import RedisError
from rest_framework import serializers
from django_redis import get_redis_connection

from utils.exceptions import logger


class SmsCodeSerializer(serializers.Serializer):
    text = serializers.CharField(label='用户输入的验证码', max_length=4, min_length=4, required=True)
    image_code_id = serializers.UUIDField(label='呈现再网页上的验证码ID')

    def validate(self, attrs):
        text = attrs.get('text')
        image_code_id = attrs.get('image_code_id')
        redis_conn = get_redis_connection('code')
        redis_text = redis_conn.get('image_code_%s' % image_code_id)
        if not redis_text:
            raise serializers.ValidationError('图片验证码过期')
        try:
            redis_conn.delete('image_code_%s' % image_code_id)
        except RedisError as e:
            logger.error(e)
        print(redis_text.decode().lower(), text)
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('验证码错误')

        return attrs





