# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: Robinson_Jim
# @time: 18-8-25 下午3:53
from rest_framework import serializers
from .models import OAuthQQUser
from users.models import User
from django_redis import get_redis_connection


class QQTokenOpenidSerializer(serializers.Serializer):
    access_token = serializers.CharField(label='操作token')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[345789]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6)

    def validate(self, attrs):
        # 校验access_token
        # 数据传递的顺序是:request.data--->attrs--->validated_data
        access_token = attrs.get('access_token')
        openid = OAuthQQUser.check_openid_from_access_token(access_token)
        if openid is None:
            raise serializers.ValidationError('无效的token')
        attrs['openid'] = openid

        # 校验手机:
        mobile = attrs.get('mobile')
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = None
        else:
            password = attrs['password']
            if not user.check_password(password):
                raise serializers.ValidationError('密码不正确')

        # 校验短信:
        redis_conn = get_redis_connection('code')
        sms_code = attrs.get('sms_code')
        redis_sms_code = redis_conn.get('sms_code_%s' % mobile)
        if not redis_sms_code:
            raise serializers.ValidationError('短信验证已过期')
        if redis_sms_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证不正确')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # 判断数据中是否有user
        user = validated_data.get('user')
        if not user:
            user = User.objects.create(
                username=validated_data.get('mobile'),
                password=validated_data.get('password'),
                mobile=validated_data.get('mobile'),
            )
            # 此时的密码还是明文,对密码进行加密:
            user.set_password(validated_data['password'])
            user.save()
        # 保存QQ授权信息:
        OAuthQQUser.objects.create(
            openid=validated_data.get('openid'),
            user=user
        )
        return user
