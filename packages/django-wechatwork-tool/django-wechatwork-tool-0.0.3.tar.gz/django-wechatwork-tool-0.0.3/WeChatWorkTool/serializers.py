import json
from django.conf import settings
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from . import models
# from WeChatWorkTool import models as tool_modesl
# from WeChatWorkTool import serializers as tool_serializers
from django.contrib.auth.models import Permission


class AccessTokenSerializer(serializers.ModelSerializer):
    """AccessToken 序列化类
    """

    class Meta:
        model = models.AccessToken
        fields = '__all__'
        depth = 3
