#coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('manager.system.views',
    (r'^carousel/$','carousel'),                # 轮播管理
)

