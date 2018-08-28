# -*- coding: utf-8 -*-
# @File  : utils.py
# @Author: Robinson_Jim
# @time: 18-8-23 下午7:51
import json
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen

from rest_framework.response import Response

from mall import settings


class OuthQQ(object):
    """
    处理跳转到QQ扫码界面的类:

    """

    def __init__(self):
        self.client_id = settings.QQ_APP_ID
        self.redirect_uri = settings.QQ_REDIRECT_URL

    def get_outh_url(self):
        # 生成auth_url
        # https://graph.qq.com/oauth2.0/authorize
        # 请求参数请包含如下内容：
        # response_type   必须      授权类型，此值固定为“code”。
        # client_id       必须      申请QQ登录成功后，分配给应用的appid。
        # redirect_uri    必须      成功授权后的回调地址，必须是注册appid时填写的主域名下的地址，建议设置为网站首页或网站的用户中心。注意需要将url进行URLEncode。
        # state           必须      client端的状态值。用于第三方应用防止CSRF攻击，成功授权后回调时会原样带回。请务必严格按照流程检查用户与state参数状态的绑定。
        # scope           可选      scope=get_user_info
        base_url = 'https://graph.qq.com/oauth2.0/authorize?'
        # 组织参数:
        params = {
            'response_type': 'code',
            # 'client_id': settings.QQ_APP_ID,
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': '/',
        }
        auth_url = base_url + urlencode(params)

        return auth_url


class QQTokenOpenid(object):
    def get_token_by_code(self, code):
        base_url = 'https://graph.qq.com/oauth2.0/token?'
        params = {
            'grant_type': 'authorization_code',
            'client_id': settings.QQ_APP_ID,
            'client_secret': settings.QQ_APP_KEY,
            'code': code,
            'redirect_uri': settings.QQ_REDIRECT_URL,
        }
        url = base_url + urlencode(params)
        # 发送请求获取响应:
        response = urlopen(url)
        # 获取响应中的数据
        data = response.read().decode()
        query_params = parse_qs(data)
        access_token = query_params.get('access_token')
        if access_token is None:
            raise Exception('获取token失败')
        return access_token[0]

    def get_openid_by_token(self, token):
        base_url = 'https://graph.qq.com/oauth2.0/me?'
        params = {
            'access_token': token,
        }
        url = base_url + urlencode(params)
        # 发送请求获取响应:
        response = urlopen(url)
        # 获取响应中的数据
        data = response.read().decode()
        # {'access_token': '916E6D0858282A8A1ABA6092EB4C73C8'}
        try:
            # 返回的数据  callback({"client_id": "YOUR_APPID", "openid": "YOUR_OPENID"})\n;
            data = json.loads(data[10:-4])
        except Exception as e:
            raise Exception('获取用户错误')
        openid = data.get('openid', None)
        return openid
