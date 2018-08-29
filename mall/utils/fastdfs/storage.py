# -*- coding: utf-8 -*-
# @File  : storage.py
# @Author: Robinson_Jim
# @time: 18-8-29 下午3:36
from django.core.files.storage import Storage
from mall import settings
from fdfs_client.client import Fdfs_client
from django.utils.deconstruct import deconstructible


@deconstructible
class FastDFSStorage(Storage):
    def __init__(self, conf_path=None, ip=None):
        if conf_path is None:
            conf_path = settings.FDFS_CLIENT_CONF
        self.conf_path = conf_path
        if ip is None:
            ip = settings.FDFS_URL
        self.ip = ip

    def _open(self, name, mode='rb'):

        pass

    def _save(self, name, content, max_length=None):
        """
        {'Local file name': '/home/jim/桌面/u=3898129523,854138783&fm=27&gp=0.jpg',
         'Uploaded size': '20.00KB',
         'Group name': 'grp1',
         'Status': 'Upload successed.',
         'Remote file_id': 'group1/M00/00/00/wKh3BFuGR6SAal1jAABR9YX_EFY776.jpg',
         'Storage IP': '192.168.119.4'}
        """
        client = Fdfs_client(self.conf_path)
        file_data = content.read()
        result = client.upload_by_buffer(file_data)
        if result.get('Status') == 'Upload successed.':
            return result.get('Remote file_id')
        else:
            raise Exception('上传失败')

    def exists(self, name):
        return False

    def url(self, name):
        return self.ip + name
