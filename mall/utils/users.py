# -*- coding: utf-8 -*-
# @File  : users.py
# @Author: Robinson_Jim
# @time: 18-8-22 下午5:48
import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_use_by_account(username):
    try:
        if re.match(r'1[345789]\d{9}', username):
            user = User.objects.get(mobile=username)
        else:
            user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证:
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_use_by_account(username)
        if user is not None and user.check_password(password):
            return user
