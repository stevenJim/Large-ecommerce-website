# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: Robinson_Jim
# @time: 18-8-22 下午2:45
import re

from rest_framework import serializers

from celery_tasks.mail.tasks import send_verify_mail
from .models import User, Address
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings


class RegisterSubmitSerializer(serializers.ModelSerializer):
    """
    用户名/密码/手机号/短信验证码/确认密码/是否同意协议
    ModelSerializer:自带create()和update()方法
    """
    sms_code = serializers.CharField(label='短信验证码', allow_null=False, allow_blank=False, write_only=True)
    password2 = serializers.CharField(label='确认密码', allow_null=False, allow_blank=False, write_only=True)
    allow = serializers.CharField(label='是否同意协议', allow_null=False, allow_blank=False, write_only=True)
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'sms_code', 'password2', 'allow', 'token')

        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # class Meta:
    #     model = User
    #     fields = ('id','username','password','mobile','password2','sms_code','allow','token')
    #     extra_kwargs = {
    #         'id': {'read_only': True},
    #         'username': {
    #             'min_length': 5,
    #             'max_length': 20,
    #             'error_messages': {
    #                 'min_length': '仅允许5-20个字符的用户名',
    #                 'max_length': '仅允许5-20个字符的用户名',
    #             }
    #         },
    #         'password': {
    #             'write_only': True,
    #             'min_length': 8,
    #             'max_length': 20,
    #             'error_messages': {
    #                 'min_length': '仅允许8-20个字符的密码',
    #                 'max_length': '仅允许8-20个字符的密码',
    #             }
    #         }
    #     }


    def validate_mobile(self, value):
        """进行单个字段的手机号:
            mobile校验
        """
        if not re.match(r'1[345789]\d{9}', value):
            raise serializers.ValidationError
        return value

    def validate_allow(self, value):
        """进行单个字段的手机号:
            allow校验
        """
        print('allow')
        if value != 'true':
            raise serializers.ValidationError
        return value

    def validate(self, attrs):
        """进行多字段校验
        1.两次密码比较是否一致;
        2.短信验证码是否和存入redis中的短信验证码一致;
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')
        sms_code = attrs.get('sms_code')
        mobile = attrs.get('mobile')

        if password != password2:
            raise serializers.ValidationError('两次输入密码不一致')
        redis_conn = get_redis_connection('code')
        #         获取redis中次号码的sms_code:
        redis_sms_code = redis_conn.get('sms_code_%s' % mobile)
        # if redis_sms_code.decode() != sms_code:
        if redis_sms_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    def create(self, validated_data):
        del validated_data['sms_code']
        del validated_data['password2']
        del validated_data['allow']

        user = super().create(validated_data)

        # 由于这样会导致一个问题就是密码是明文,不利于加密管理:系统的user自带一个加密的方法set_password()
        user.set_password(validated_data['password'])
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class EmailSerializer(serializers.ModelSerializer):
    """
    邮箱序列化器
    """

    class Meta:
        model = User
        fields = ('id', 'email')
        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        instance.email = email
        instance.save()
        """用户保存邮箱后:
        1.生成验证url;

        2.发送验证邮件;
        """

        # 1.生成验证url;
        verify_url = instance.generate_verify_email_url()

        # 2.发送验证邮件;
        send_verify_mail.delay(email, verify_url)

        return instance


class AddressSerializer(serializers.ModelSerializer):

    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def create(self, validated_data):
        # Address模型类中有user属性,将user对象添加到模型类的创建参数中
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
