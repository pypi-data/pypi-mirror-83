import datetime
import json

import requests
from django.db import models

# WeCHatWor API URL
BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/"


# Create your models here.
class AccessToken(models.Model):
    """企业微信access_token
    """
    appname = models.CharField(max_length=128, verbose_name='appname')
    appid = models.CharField(max_length=128, verbose_name='appid')
    corpid = models.CharField(max_length=128, verbose_name='corpid')  # corpid
    appsecret = models.CharField(max_length=256, verbose_name='APPSECRET')
    expires_in = models.DateTimeField(verbose_name='expires_in', auto_now=False, auto_now_add=False)  # 过期时间
    token = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name='token',
                             db_index=True)  # access_token 这里要注意长度，太短存储会失败 token官方给出的长度是512个字符空间
    call_back_url = models.URLField(null=True, blank=True)
    call_back_token = models.CharField(max_length=256, null=True, blank=True)
    call_back_key = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = '企业微信access_token信息'
        verbose_name_plural = verbose_name

    def request_access_token(self):
        """request access_token
        """
        res = requests.get(BASE_URL + 'gettoken',
                           {'corpid': self.corpid, 'corpsecret': self.appsecret}
                           )
        data = json.loads(res.content.decode('utf-8'))
        return data

    def get_access_token(self):
        """get access_token by model
        """
        datetime_now = datetime.datetime.now()

        if self.expires_in <= datetime_now:
            data = self.request_access_token()
            if 'access_token' in data:
                expires_in = (datetime.datetime.now(
                ) + datetime.timedelta(seconds=int(data['expires_in']))).strftime('%Y-%m-%d %H:%M:%S')
                self.expires_in = expires_in
                self.token = data['access_token']
                self.save()
                return self.token
            else:
                return None
        else:
            return self.token
