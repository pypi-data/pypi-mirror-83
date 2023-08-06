#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @File        :tool
    @Description :
    @DateTiem    :2020/7/27 14:25
    @Author      :Jay Zhang
"""

import datetime
import json
import urllib
import uuid

import requests  # python http请求模块
import xml.etree.cElementTree as ET
from . import models, WXBizMsgCrypt3

# WeCHatWor API URL
BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin/"


class InputError(Exception):
    """Exception raised for errors in the input
    """

    def __init__(self, message):
        self.message = message


def Xml2Dict(xml):
    """Xml to Dict

    :param xml:Xml
    :return:Dict data
    """
    xml_tree = ET.fromstring(xml)
    data = {}
    for item in xml_tree.iter():
        if item.tag != "xml":
            data[item.tag] = item.text
    return data


class TextMessageObject:
    """Message Object"""

    def __init__(self, content):
        self.msgtype = "text"
        self.content = content

    def data(self):
        """return data"""
        data = {
            "content": self.content
        }
        return data


class MediaMessageObject:
    """MediaMessageObject"""

    def __init__(self, msgtype, mediaid, title=None, description=None):
        if msgtype not in ['image', 'voice', 'video', 'file']:
            return InputError(message="msgtype must in 'image','voice','video','file'")
        self.msgtype = msgtype
        self.mediaid = mediaid
        self.title = title
        self.description = description

    def data(self):
        """return data"""
        if self.msgtype == 'video':
            data = {
                "media_id": self.mediaid,
                "title": self.title,
                "description": self.description
            }
        else:
            data = {
                "media_id": self.mediaid
            }
        return data


class TextCardMessageObject:
    """TextCardMessageObject"""

    def __init__(self, title, description, url, btntxt=None):
        self.msgtype = 'textcard'
        self.title = title
        self.description = description
        self.url = url
        self.btntext = btntxt

    def data(self):
        """return data"""
        data = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "btntext": self.btntext
        }
        return data


class NewsMessageObject:
    """NewsMessageObject"""

    def __init__(self, title, description, url, picurl):
        self.msgtype = 'textcard'
        self.title = title
        self.description = description
        self.url = url
        self.picurl = picurl

    def data(self):
        """return data"""
        data = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "picurl": self.picurl
        }
        return data


class MarkDownMessageObject:
    """MarkDownMessageObject"""

    def __init__(self, content):
        self.msgtypr = 'markdown'
        self.content = content

    def data(self):
        """return data"""
        data = self.content
        return data


class TaskCardBtnTemplate:
    """TaskCard Button Template"""

    def __init__(self, key, name, replace_name=None, color=None, is_bold=False):
        self.data = {
            "key": key,
            "name": name,
            "replace_name": replace_name,
            "color": color,
            "is_bold": is_bold
        }


class TaskCardMessageObject:
    """TaskCardMessageObject"""

    def __init__(self, title, description, url, btn_list: [TaskCardBtnTemplate], task_id=None):
        self.msgtype = 'taskcard'
        self.title = title
        self.description = description
        self.url = url
        self.btn = btn_list
        self.task_id = task_id if task_id else str(uuid.uuid1())

    def data(self):
        """return data"""
        data = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "task_id": self.task_id,
            "btn": self.btn
        }
        return data


class CorpApp:
    """
    WeChatWorks custom application
    """

    def __init__(self, appname):
        try:
            self.access_token = models.AccessToken.objects.get(appname=appname).get_access_token()
            self.at = models.AccessToken.objects.get(appname=appname)
        except Exception as er:
            print('er', er)
            self.access_token = None

    def app_info(self):
        """
        get this app info
        :return: App Info
        """
        res = requests.get(BASE_URL + 'agent/get',
                           {'access_token': self.access_token, 'agentid': self.at.appid}
                           )
        data = json.loads(res.content.decode('utf-8'))
        if data['errcode'] == 0 and data['errmsg'] == "ok":
            data.pop('errcode')
            data.pop('errmsg')
            return data
        else:
            return None

    def get_userid_by_code(self, code):
        """get userid by code，It's just for webpage authorization link

        :param code: in webpage authorization link
        :return:UserId
        """
        res = requests.get(BASE_URL + 'user/getuserinfo',
                           {'access_token': self.access_token, 'code': code}
                           )
        data = json.loads(res.content.decode('utf-8'))
        if data['errcode'] == 0 and data['errmsg'] == "ok":
            return data['UserId']
        else:
            return None

    def get_user(self, userid):
        """get user info

        :param userid: WeChatWork user's id
        :return: a dict that user info
        """
        res = requests.get(BASE_URL + 'user/get',
                           {'access_token': self.access_token, 'userid': userid}
                           )
        data = json.loads(res.content.decode('utf-8'))
        if data['errcode'] == 0 and data['errmsg'] == "ok":
            data.pop('errcode')
            data.pop('errmsg')
            return data
        else:
            return None

    def get_user_tag_list(self):
        """get user tag list

        :return: user tag list
        """
        res = requests.get(BASE_URL + 'tag/list', {'access_token': self.access_token})
        data = json.loads(res.content.decode('utf-8'))
        if data['errcode'] == 0 and data['errmsg'] == "ok":
            data.pop('errcode')
            data.pop('errmsg')
            return data
        else:
            return None

    def get_tag_user_simplelist(self, tagid):
        """get user list

        :param tagid:
        :return:
        """
        res = requests.get(BASE_URL + 'tag/get', {'access_token': self.access_token, 'tagid': tagid})
        data = json.loads(res.content.decode('utf-8'))
        if data['errcode'] == 0 and data['errmsg'] == "ok":
            data.pop('errcode')
            data.pop('errmsg')
            return data
        else:
            return None

    def get_department_user_simplelist(self, department_id, fetch_child=False):
        """get user simplelist by department id

        :param department_id:
        :param fetch_child:
        :return
            For success example:
                {
                    "errcode" : 0,
                    "errmsg" : "ok",
                    "invaliduser" :"",
                    "invalidparty" : "",
                    "invalidtag": ""
                }

            For error example:
                {
                    "errcode" : 0,
                    "errmsg" : "ok",
                    "invaliduser" : [userid1,userid2],
                    "invalidparty" : [partyid1,partyid2],
                    "invalidtag": [tagid1,tagid2]
                }
        """
        res = requests.get(BASE_URL + 'user/simplelist',
                           {'access_token': self.access_token, 'department_id': department_id,
                            'fetch_child': 1 if fetch_child else 0}
                           )
        data = json.loads(res.content.decode('utf-8'))
        if data['errcode'] == 0 and data['errmsg'] == "ok":
            return data['userlist']
        else:
            return None

    def get_department_user_list(self, department_id, fetch_child=False):
        """get user list by department id

        :param department_id:
        :param fetch_child:
        :return:
        """
        res = requests.get(BASE_URL + 'user/list',
                           {'access_token': self.access_token, 'department_id': department_id,
                            'fetch_child': 1 if fetch_child else 0}
                           )
        data = json.loads(res.content.decode('utf-8'))
        if data['errcode'] == 0 and data['errmsg'] == "ok":
            return data['userlist']
        else:
            return None

    def get_department(self, id):
        """get department info list

        :param id: WeChatWork department's id
        :return:
        """
        res = requests.get(BASE_URL + 'department/list',
                           {'access_token': self.access_token, 'id': id}
                           )
        data = json.loads(res.content.decode('utf-8'))
        if data['errcode'] == 0 and data['errmsg'] == "ok":
            return data['department']
        else:
            return None

    def SendMsg(self, msgobj, touser: list = [], toparty: list = [], totag: list = [],
                safe=0, enable_id_trans=0,
                enable_duplicate_check=0,
                duplicate_check_interval=1800):
        """

        :param touser:
        :param toparty:
        :param totag:
        :param msgobj:
        :param safe:
        :param enable_id_trans:
        :param enable_duplicate_check:
        :param duplicate_check_interval:
        :return:
        """
        if touser is [] and toparty is [] and totag is []:
            return InputError(message="touser, toparty, totag cannot be empty at the same time")
        else:
            msg_data = {
                "touser": "|".join(str(i) for i in touser),
                "toparty": "|".join(str(i) for i in toparty),
                "totag": "|".join(str(i) for i in totag),
                "msgtype": msgobj.msgtype,
                "agentid": self.at.appid,
                "safe": safe,
                msgobj.msgtype: msgobj.data(),
                "enable_id_trans": enable_id_trans,
                "enable_duplicate_check": enable_duplicate_check,
                "duplicate_check_interval": duplicate_check_interval
            }
            # print(msg_data)
            msg_data = json.dumps(msg_data)
            res = requests.post(BASE_URL + 'message/send' + '?access_token=' + self.access_token, msg_data)
            data = json.loads(res.content.decode('utf-8'))
            if data['errcode'] == 0 and data['errmsg'] == "ok":
                return data
            else:
                if 'invaliduser' in data:
                    data['invaliduser'] = data['invaliduser'].split('|')
                if 'invalidparty' in data:
                    data['invalidparty'] = data['invalidparty'].split('|')
                if 'invalidtag' in data:
                    data['invalidtag'] = data['invalidtag'].split('|')
                return data

    def call_back_data(self, url_data, body_data):
        """call back data decode

        :param url_data: this call back data(msg_signature,timestamp,nonce) in url
        :param body_data: this call back post body data
        :return: xml context
        """
        ret, xml_content = WXBizMsgCrypt3.WXBizMsgCrypt(self.at.call_back_token, self.at.call_back_key,
                                                        self.at.corpid).DecryptMsg(body_data, url_data['msg_signature'],
                                                                                   url_data['timestamp'],
                                                                                   url_data['nonce'])
        data = Xml2Dict(xml_content)
        # print(data)
        return data


def call_back_verify(data, appname=None, url=None):
    """verify the call back URL

    :param data: dict{msg_signature,timestamp,nonce,echostr}
    :param appname: appname (appname,url can't be empty at the same time)
    :param url: rquest url
    :return:
    """
    if url is None and appname is None:
        return InputError(message="appname,url can't be empty at the same time")
    elif url:
        try:
            at = models.AccessToken.objects.get(call_back_url=url)
        except Exception as e:
            # print(e)
            return e
    else:
        try:
            at = models.AccessToken.objects.get(appname=appname)
        except Exception as e:
            # print(e)
            return e
    try:
        msg_signature = data['msg_signature']
        timestamp = data['timestamp']
        nonce = data['nonce']
        echostr = data['echostr']
        ret, sReplyEchoStr = WXBizMsgCrypt3.WXBizMsgCrypt(at.call_back_token, at.call_back_key, at.corpid).VerifyURL(
            msg_signature, timestamp, nonce, echostr)
        return sReplyEchoStr
    except Exception as e:
        # print(e)
        return e
