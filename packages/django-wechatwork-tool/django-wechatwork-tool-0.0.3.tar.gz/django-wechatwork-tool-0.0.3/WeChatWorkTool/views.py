"""
@File        :permission.py
@Description :企业微信Auth
@DateTiem    :2020-04-18 10:49:05
@Author      :Jay Zhang
"""
import json
import urllib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import tool


# Create your views here.
@csrf_exempt
def call_back(request):
    """WeChatWork messqge callback Simple Example"""
    if request.method == 'GET':
        # Authentication  url
        data = request.GET.dict()
        return HttpResponse(tool.call_back_verify(data, 'sap'))

    if request.method == 'POST':
        url_data = request.GET.dict()
        cb = tool.CorpApp('sap').call_back_data(url_data, request.body)
        return HttpResponse(json.dumps(cb), content_type="application/json")
