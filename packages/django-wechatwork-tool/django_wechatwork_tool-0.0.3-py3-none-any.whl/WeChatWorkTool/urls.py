from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('wechatwork_callback/', views.call_back),  # 回调信息
]
